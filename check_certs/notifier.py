import requests


def alert(reason: str) -> None:
    print(f"ALERT: {reason}")


def send_telegram(domain: str, days_left: int, token: str, chat_id: str) -> None:
    if not token or not chat_id:
        print("Telegram config is missing. Skipping notification.")
        return

    try:
        message = (
            f"SSL Expiring Soon\\n"
            f"Domain: {domain}\\n"
            f"Expires in: {days_left} days"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
        }
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        print("Telegram alert sent.")
    except requests.RequestException as e:
        print(f"Telegram send failed: {e}")
