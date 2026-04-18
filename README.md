# SSL Certificate Checker Telegram Bot

Simple Python bot that checks SSL certificate expiry for multiple domains and sends alerts to Telegram.
It is designed to run automatically with GitHub Actions every day.

## Features

- Checks SSL certificates for multiple domains on port 443
- Sends Telegram alerts when certificate expiry is near (7 days, 3 days, and 24 hours)
- Avoids duplicate alerts with a local state file
- Supports manual run (`workflow_dispatch`) and scheduled run in GitHub Actions

## How It Works

1. Load domains from `data/domains.json`.
2. Connect to each domain and read certificate expiry date.
3. Calculate remaining time.
4. If expiry is close (7d / 3d / 24h), send Telegram message.
5. Save sent alert levels in `data/alert_state.json` to avoid duplicates for the same certificate.
6. If certificate changes (new expiry date), alert levels reset for that domain.

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd check-certs
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_telegram_chat_id
```

## Run Locally

```bash
python main.py
```

You should see logs for each domain, including days/hours left and alert status.

## GitHub Actions

Workflow file: `.github/workflows/check-cert.yml`

- Runs on schedule: `0 0 * * *` (daily at 00:00 UTC)
- Can also be run manually from the Actions tab (`workflow_dispatch`)
- Uses repository secrets for Telegram config: `TELEGRAM_TOKEN` and `TELEGRAM_CHAT_ID`

Behavior in CI:

- Action starts a fresh runner each run.
- If a domain is unreachable from GitHub-hosted runners, that check can fail or timeout.
- The script continues checking other domains.

## Add New Domains

Edit `data/domains.json`:

```json
{
	"domains": [
		"example.com",
		"api.example.com",
		"another-domain.com"
	]
}
```

Tips:

- Use hostname only (no `https://`)
- Make sure the domain serves TLS on port 443

## Known Limitations

- Internal/private domains may not be reachable from GitHub Actions runners.
- Network issues and TLS handshake problems can cause timeouts.
- Alert state is file-based; it is simple and local to the run environment.

## Contributing

1. Fork the repository.
2. Create a branch using `feature/<short-description>` or `fix/<short-description>`.
3. Make your changes.
5. Open a pull request and include what changed.

## Future Improvements

- Add retry logic for temporary network failures
- Add optional per-domain timeout settings
- Add support for custom alert thresholds
- Store alert state in a persistent backend (for better CI continuity)
