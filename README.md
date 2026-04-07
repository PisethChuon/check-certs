# Check Certs

Check Certs monitors SSL/TLS certificate expiration for your domains and sends Telegram alerts before certificates expire.
It helps prevent downtime and surprise incidents caused by expired certificates.

## Project Structure

```text
check-certs/
├── check_certs/
│   ├── __init__.py
│   ├── config.py
│   ├── domain_loader.py
│   ├── notifier.py
│   ├── runner.py
│   └── ssl_checker.py
├── data/
│   └── domains.json
├── main.py
├── requirements.txt
└── README.md
```

## Setup

### Prerequisites

- Python 3.10+
- A Telegram bot token
- A Telegram chat ID for notifications

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `.env` in the project root:

```env
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

3. Add domains to `data/domains.json`:

```json
{
	"domains": [
		"google.com",
		"example.com"
	]
}
```

4. Run:

```bash
python main.py
```

### Expected behavior

The script checks each configured domain certificate and notifies your Telegram chat when a certificate is near expiry.

## Next Feature

- `feature/ssl-renewal-notification`: Add reminder notifications ahead of certificate renewal windows so teams can plan and renew certificates before hard expiry.

## Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Make your changes with clear commit messages.
4. Open a pull request describing what changed, why it changed, and how you tested it.

If possible, include tests or a reproducible example for bug fixes.
