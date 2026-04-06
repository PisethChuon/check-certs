# Check Certs

Simple SSL certificate expiry checker with Telegram alerts.

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
