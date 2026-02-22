# About
An SSL certificate monitoring application that delivers automated expiration alerts via Telegram, enabling website owners to proactively manage renewal schedules.

1. Goal
Alert at 7 days before expire

2. Scop
First version:
- Check SSL for many domains
- Run automatically on a schedule
- Send message only to Telegram

Later version:
- Add email

3. Stack
Language: Python
SSL check: ssl + socket or cryptography
Scheduler: cron or APScheduler
Telegram: Telegram Bot API
Storage:
    v1: JSON file
    v2: SQLite or PostgreSQL

4. System flow
    1. Scheduler triggers job (daily)
    2. Scrip checks SSL expiry date
    3. Calculate days left
    4. If days match alert rule --> send Telegram message
    5. Log result

5. SSL checking logic (core part)
What I need from SSL
- Domain name
- Expiration date
- Days remaining

Pseudo logic:

connect to domain:443
read certificate
get "notAfter" date
calculate days-left

6. Telegram bot setup
Tasks:
- Create bot with BotFather
- Get BOT_TOKEN
- Get CHAT_ID of owner

Message format example:
SSL Alert
Domain: example.com
Expires in: 7 days
Expiry date: 2026-01-14

7. Configuration design
Avoid hardcoding

```
domains:
- example.com
- mysite.org

alert_days:
- 30
- 7
- 1

8. Scheduling strategy
Simple options:
 - Cron (recommended for server)
    - Run once perday
- APScheduler
    - Good if bundled in one app

9. Error handling (don’t skip this)
Handle cases:
    - Domain unreachable
    - SSL not found
    - Timeout
    - Telegram API failure
Log everything.

10. Testing plan
Before production:
- Test with an expired SSL domain
- Test with a valid long-term SSL
- Test Telegram message delivery
- Test duplicate alerts (avoid spam)

11. Deployment plan
Basic:
- VPS (Ubuntu)
- Python virtualenv
- Cron job
- .env for secrets

12. Future improvements (keep in mind)
- Web UI to manage domains
- Multi-user Telegram support
- SSL issuer info
- Auto-renew reminder link
- Prometheus / Grafana metrics