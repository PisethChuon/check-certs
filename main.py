import ssl
import socket
import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone
from pathlib import Path

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
TELEGRAM_CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

DOMAINS_FILE = Path(__file__).resolve().parent / "domains.json"


def load_domains(domains_file: Path = DOMAINS_FILE) -> list[str]:
    try:
        with domains_file.open("r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Domains file not found: {domains_file}")
        return []
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in domains file: {e}")
        return []

    if isinstance(data, dict):
        domains = data.get("domains", [])
    elif isinstance(data, list):
        domains = data
    else:
        print("Domains JSON must be a list or an object with a 'domains' list.")
        return []

    if not isinstance(domains, list):
        print("The 'domains' value must be a list.")
        return []

    cleaned_domains = [d.strip() for d in domains if isinstance(d, str) and d.strip()]
    if not cleaned_domains:
        print("No valid domains found in domains file.")
    return cleaned_domains

def check_ssl(domain: str):
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
        days_left  = diff.days
        hours_left = diff.total_seconds() / 3600

        print(f"Expiry date: {expiry_date.strftime('%Y-%m-%d')}")
        print(f"Days left:   {days_left}")
        print(f"Hours left:  {hours_left:.1f}")

        check_alert(domain, days_left, hours_left)

    except socket.timeout:
        print(f"[{domain}] Connection timed out")
    except ssl.SSLError as e:
        print(f"[{domain}] SSL error: {e}")
    except Exception as e:
        print(f"[{domain}] Unexpected error: {e}")

def check_alert(domain: str, days_left: int, hours_left: float):
    if hours_left <= 24:
        send_telegram(domain, days_left)
        alert("Under 24 hours!")
    elif days_left <= 3:
        send_telegram(domain, days_left)
        alert("3-day warning")
    elif days_left <= 7:
        send_telegram(domain, days_left)
        alert("7-day warning")

def alert(reason: str):
    print(f"ALERT: {reason}")

def send_telegram(domain: str, days_left: int):
    try:
        message = (
            f"SSL Expiring Soon\n"
            f"Domain: {domain}\n"
            f"Expires in: {days_left} days"
        )
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message
        }
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        print("Telegram alert sent.")
    except requests.RequestException as e:
        print(f"Telegram send failed: {e}")


def main():
    domains = load_domains()
    for domain in domains:
        print(f"\nChecking {domain}...")
        check_ssl(domain)


if __name__ == "__main__":
    main()