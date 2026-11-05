# 🤖 Bahoush Tech Telegram Bot

Official Telegram bot for **Bahoush Tech** — delivering website services via Telegram.

- **Bot:** [@bahoushtechbot](https://t.me/bahoushtechbot)
- **Website:** [bahoushtech.com](https://bahoushtech.com)
- **Instagram:** [@bahoushtech](https://instagram.com/bahoushtech)

## Status

🚧 In development — Phase 0 (scaffold) complete, Phase 1 (core bot) next.

## Tech Stack

| Layer | Tech |
|-------|------|
| Language | Python 3.13 |
| Framework | python-telegram-bot v21+ |
| Database | SQLite |
| Config | python-dotenv |

## Quick Start

\`\`\`bash
git clone https://github.com/benyaminsmart/bahoushtechbot.git
cd bahoushtechbot
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
nano .env   # add BOT_TOKEN
python -m src.main
\`\`\`

## Structure

\`\`\`
src/        bot code (handlers, keyboards, services, database, utils)
docs/       architecture docs
scripts/    automation
data/       SQLite DB (gitignored)
logs/       log files (gitignored)
\`\`\`

## Roadmap

- [x] Phase 0 — Scaffold
- [ ] Phase 1 — Core bot (/start, /help, main menu)
- [ ] Phase 2 — Service catalog
- [ ] Phase 3 — Contact form
- [ ] Phase 4 — Admin panel
- [ ] Phase 5 — DB persistence
- [ ] Phase 6 — Deploy & monitor

© Bahoush Tech
