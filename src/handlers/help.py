"""/help handler — list all commands."""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from src.keyboards.main_menu import main_menu_reply_keyboard


HELP_TEXT = (
    "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    "┃   <b>◆ HELP — Commands ◆</b>   ┃\n"
    "┗━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
    "<b>Available commands:</b>\n\n"
    "/start — Main menu\n"
    "/help — This help message\n"
    "/services — Browse our 5 services\n"
    "/projects — Browse our 6 projects\n"
    "/ai — Chat with Mr. Computer (AI)\n"
    "/reset — Reset AI conversation\n"
    "/form — Start a project request\n"
    "/contact — Contact information\n"
    "/about — About Bahoush Tech\n"
    "/cancel — Cancel current operation\n\n"
    "◈ ━━━━━━━━━━━━━━━━━━━━━ ◈\n"
    "<i>Need help? Email us at info@bahoushtech.com</i>"
)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help."""
    await update.message.reply_text(
        HELP_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_reply_keyboard(), # Show the bottom menu so user can navigate back
    )
