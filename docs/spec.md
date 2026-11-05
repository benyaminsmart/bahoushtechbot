# Spec — Bahoush Tech Telegram Bot

**Bot:** @bahoushtechbot
**Brand:** BAHOUSH TECH
**Language:** English only
**Design:** Unicode + Emoji + Banner Image (modern, professional)
**AI Backend:** Groq API (`openai/gpt-oss-20b`)

## 1. Overview
A Telegram bot that mirrors bahoushtech.com — same content, same services,
same AI assistant (Mr. Computer), same portfolio — optimized for Telegram UX.

## 2. Main Menu (`/start`)
Sent as: banner image + caption + inline keyboard.

Inline keyboard (4 rows × 2 columns):
| Row 1 | 🛠 Services | 💼 Projects |
| Row 2 | 🧠 Mr. Computer | 🚀 Start Project |
| Row 3 | ℹ️ About Us | 📞 Contact |
| Row 4 | 🌐 Website | 📸 Instagram |

## 3. Commands
/start, /help, /services, /projects, /ai, /reset, /form, /contact, /about, /cancel, /admin

## 4. Services Flow
5 services (AI, Web2, Web3, Bots, UI/UX). Each with details + buttons
[🚀 Request Consultation] [🌐 View on site] [« Back].

## 5. Projects Flow
6 projects (Platform-X, WORD SMART, BahoushGuard, StaySync, Bahoush Media, Mr. Computer).
Each with status (🟡🟢🟠), tagline, description, tags, + [🌐 View on site] [« Back].

## 6. Mr. Computer (AI Chat)
- Entry: /ai, /mrcomputer, or button
- Groq API with system prompt
- History in memory (last 10 messages/user)
- Rate limit 1/2s
- /reset clears
- Typing indicator + Markdown

## 7. Start Project Form (7 steps)
1. Full name
2. Email
3. Service type (5 options)
4. Product type (3 options)
5. Delivery (2 options)
6. Budget (5 options)
7. Details (/skip allowed)

UI: each step = separate message with progress bar `▰▰▰▱▱▱▱`,
[« Back] [✖ Cancel]. On submit → save SQLite + notify admin + success message.

## 8. Contact Flow
/contact → email, location, social links, [Message us directly].

## 9. About Flow
/about → tagline, intro, 5 domains, [Our Vision] [Our Values] [🌐 Visit site] [« Back].

## 10. Admin Panel (/admin)
Only IDs in ADMIN_IDS env.
Menu: [📥 New Requests] [📊 Stats] [📢 Broadcast] [👥 Users]

## 11. Language
English only.

## 12. Tech Stack
- python-telegram-bot v21.6 (async)
- SQLite via aiosqlite
- Groq API (openai/gpt-oss-20b)
- python-dotenv
- Termux (dev) → VPS (prod)
- Polling (dev) → Webhook (prod, optional)

## 13. Project Structure
src/{content,handlers,keyboards,services,database,utils}/ + main.py
assets/images/ + data/ + logs/ + docs/ + scripts/

## 14. Phases
0 ✅ Infrastructure, Git, content extraction
1 🔄 Core bot: /start, /help, main menu, banner
2 ⏳ Services & Projects flows
3 ⏳ Mr. Computer AI chat
4 ⏳ Start Project form + SQLite + admin notify
5 ⏳ Contact & About flows
6 ⏳ Admin panel (requests, stats, broadcast)
7 ⏳ Deploy, monitor, polish

## 15. Security
- Tokens/keys in .env only
- Admin auth by numeric ID
- Rate limiting on AI (1/2s)
- Input validation on all forms
- No user data leaked between users

## 16. Environment Variables
BOT_TOKEN, ADMIN_IDS, GROQ_API_KEY (+ others, see .env.example)
