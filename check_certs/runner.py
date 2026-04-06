from .config import TELEGRAM_CHAT_ID, TELEGRAM_TOKEN, get_domains_file
from .domain_loader import load_domains
from .ssl_checker import check_ssl


def main() -> None:
    domains = load_domains(get_domains_file())
    for domain in domains:
        print(f"\\nChecking {domain}...")
        check_ssl(domain, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID)
