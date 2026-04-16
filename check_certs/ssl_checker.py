import socket
import ssl
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import ALERT_STATE_FILE
from .notifier import alert, send_telegram


def _load_alert_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}

    try:
        with path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
            if isinstance(data, dict):
                return data
    except (OSError, json.JSONDecodeError):
        pass

    return {}


def _save_alert_state(path: Path, state: dict[str, Any]) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            json.dump(state, fh, indent=2, sort_keys=True)
    except OSError as e:
        print(f"Failed to save alert state: {e}")


def _get_alert_level(days_left: int, hours_left: float) -> tuple[str, str] | None:
    if hours_left <= 24:
        return ("24h", "Under 24 hours!")
    if days_left <= 3:
        return ("3d", "3-day warning")
    if days_left <= 7:
        return ("7d", "7-day warning")
    return None


def check_alert(
    domain: str,
    days_left: int,
    hours_left: float,
    expiry_label: str,
    expiry_key: str,
    token: str,
    chat_id: str,
) -> None:
    alert_level = _get_alert_level(days_left, hours_left)
    if alert_level is None:
        return

    level_code, reason = alert_level
    state = _load_alert_state(ALERT_STATE_FILE)
    domain_state = state.get(domain, {})
    saved_expiry_key = domain_state.get("expiry")

    if saved_expiry_key != expiry_key:
        domain_state = {"expiry": expiry_key, "sent_levels": []}

    sent_levels = set(domain_state.get("sent_levels", []))
    if level_code in sent_levels:
        print(f"[{domain}] {level_code} alert already sent. Skipping duplicate.")
        return

    sent = send_telegram(domain, days_left, expiry_label, token, chat_id)
    if not sent:
        return

    alert(reason)
    sent_levels.add(level_code)
    domain_state["sent_levels"] = sorted(sent_levels)
    state[domain] = domain_state
    _save_alert_state(ALERT_STATE_FILE, state)


def check_ssl(domain: str, token: str, chat_id: str) -> None:
    try:
        ctx = ssl.create_default_context()
        sock = socket.socket()
        sock.settimeout(5)
        with ctx.wrap_socket(sock, server_hostname=domain) as s:
            s.connect((domain, 443))
            cert = s.getpeercert()

        expiry_str = cert["notAfter"]
        expiry_date = datetime.strptime(expiry_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
        expiry_label = f"{expiry_date.strftime('%A, %B')} {expiry_date.day}"
        expiry_key = expiry_date.isoformat()
        now = datetime.now(timezone.utc)
        diff = expiry_date - now
        days_left = diff.days
        hours_left = diff.total_seconds() / 3600

        print(f"Expiry date: {expiry_date.strftime('%Y-%m-%d')}")
        print(f"Days left:   {days_left}")
        print(f"Hours left:  {hours_left:.1f}")

        check_alert(domain, days_left, hours_left, expiry_label, expiry_key, token, chat_id)

    except socket.timeout:
        print(f"[{domain}] Connection timed out")
    except ssl.SSLError as e:
        print(f"[{domain}] SSL error: {e}")
    except Exception as e:
        print(f"[{domain}] Unexpected error: {e}")
