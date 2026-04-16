import requests


def alert(reason: str) -> None:
    print(f"ALERT: {reason}")


def send_telegram(domain: str, days_left: int, expiry_label: str, token: str, chat_id: str) -> bool:
    if not token or not chat_id:
        print("Telegram config is missing. Skipping notification.")
        return False

    try:
        message = (
            f"🔴 SSL Certificate Alert\n"
            f"Domain: {domain}\n"
            f"Expires: {expiry_label}\n"
            f"Time left: {days_left} days"
        )
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
        }
        resp = requests.post(url, json=payload, timeout=5)
        resp.raise_for_status()
        print("Telegram alert sent.")
        return True
    except requests.RequestException as e:
        print(f"Telegram send failed: {e}")
        return False
