import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[1]
PRIMARY_DOMAINS_FILE = BASE_DIR / "data" / "domains.json"
LEGACY_DOMAINS_FILE = BASE_DIR / "domains.json"
ALERT_STATE_FILE = BASE_DIR / "data" / "alert_state.json"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")


def get_domains_file() -> Path:
    if PRIMARY_DOMAINS_FILE.exists():
        return PRIMARY_DOMAINS_FILE
    return LEGACY_DOMAINS_FILE
