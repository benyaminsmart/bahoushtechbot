""" /start handler — sends banner + main menu."""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.keyboards.main_menu import main_menu_reply_keyboard
from src.utils.config import config
from src.utils.logger import log


WELCOME_TEXT = (
    "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    "┃   ◆ <b>BAHOUSH TECH</b> ◆   ┃\n"
    "┃   <i>Turn Ideas Into Reality</i>   ┃\n"
    "┗━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
    "🤖 <b>Welcome to BAHOUSH TECH!</b>\n\n"
    "Intelligent digital solutions engineered for the future.\n"
    "From AI-powered platforms to Web2 and Web3 solutions — "
    "we build digital experiences that help businesses evolve.\n\n"
    "◈ ━━━━━━━━━━━━━━━━━━━━━ ◈\n"
    "<i>Choose an option from the menu below ⬇️</i>"
)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start — send banner + welcome + main menu."""
    user = update.effective_user
    log.info(f"/start from {user.id} (@{user.username or 'no_username'})")

    # Clear any pending state
    context.user_data.clear()

    # 1. Send banner + text
    try:
        if config.BANNER_PATH.exists():
            with open(config.BANNER_PATH, "rb") as banner:
                await update.message.reply_photo(
                    photo=banner,
                    caption=WELCOME_TEXT,
                    parse_mode=ParseMode.HTML,
                )
        else:
            await update.message.reply_text(WELCOME_TEXT, parse_mode=ParseMode.HTML)
    except Exception as e:
        log.warning(f"Failed to send banner: {e}")
        await update.message.reply_text(WELCOME_TEXT, parse_mode=ParseMode.HTML)

    # 2. Send the bottom keyboard as a separate message
    await update.message.reply_text(
        "⬇️ <b>Main Menu</b>",
        parse_mode=ParseMode.HTML,
        reply_markup=main_menu_reply_keyboard(),
    )
