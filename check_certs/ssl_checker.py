import socket
import ssl
from datetime import datetime, timezone

from .notifier import alert, send_telegram


def check_alert(domain: str, days_left: int, hours_left: float, token: str, chat_id: str) -> None:
    if hours_left <= 24:
        send_telegram(domain, days_left, token, chat_id)
        alert("Under 24 hours!")
    elif days_left <= 3:
        send_telegram(domain, days_left, token, chat_id)
        alert("3-day warning")
    elif days_left <= 7:
        send_telegram(domain, days_left, token, chat_id)
        alert("7-day warning")


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
        now = datetime.now(timezone.utc)
        diff = expiry_date - now
        days_left = diff.days
        hours_left = diff.total_seconds() / 3600

        print(f"Expiry date: {expiry_date.strftime('%Y-%m-%d')}")
        print(f"Days left:   {days_left}")
        print(f"Hours left:  {hours_left:.1f}")

        check_alert(domain, days_left, hours_left, token, chat_id)

    except socket.timeout:
        print(f"[{domain}] Connection timed out")
    except ssl.SSLError as e:
        print(f"[{domain}] SSL error: {e}")
    except Exception as e:
        print(f"[{domain}] Unexpected error: {e}")
