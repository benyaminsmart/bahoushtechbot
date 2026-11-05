"""Bahoush Tech Bot — entry point."""

import sys
import traceback
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.handlers.start import start_command
from src.handlers.help import help_command
from src.keyboards.main_menu import main_menu_reply_keyboard
from src.utils.config import config
from src.utils.logger import log


async def handle_menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages sent from the Reply Keyboard."""
    text = update.message.text
    
    placeholders = {
        "🛠 Services": "🛠 <b>Services</b>\n\n<i>Coming in Phase 2...</i>",
        "💼 Projects": "💼 <b>Projects</b>\n\n<i>Coming in Phase 2...</i>",
        "🧠 Mr. Computer": "🧠 <b>Mr. Computer</b>\n\n<i>Coming in Phase 3...</i>",
        "🚀 Start Project": "🚀 <b>Start Project</b>\n\n<i>Coming in Phase 4...</i>",
        "📺 Bahoush Media": "📺 <b>Bahoush Media</b>\n\n<i>Coming in Phase 2...</i>",
        "ℹ️ About Us": "ℹ️ <b>About Us</b>\n\n<i>Coming in Phase 5...</i>",
        "📞 Contact": "📞 <b>Contact</b>\n\n<i>Coming in Phase 5...</i>",
    }

    if text in placeholders:
        await update.message.reply_text(placeholders[text], parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(
            "🤖 I didn't understand that. Please use the menu below.",
            reply_markup=main_menu_reply_keyboard()
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors."""
    log.error(f"Update {update} caused error {context.error}")


def main() -> None:
    """Start the bot."""
    print("⏳ 1. Validating config...")
    config.validate()
    
    print("⏳ 2. Building application...")
    app = Application.builder().token(config.BOT_TOKEN).build()

    print("⏳ 3. Adding handlers...")
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_text))
    app.add_error_handler(error_handler)

    print("🚀 4. Bot is running! Go to Telegram and press /start")
    print("🛑 Press Ctrl+C to stop.\n")
    
    # This line keeps the bot running
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n❌ ❌ ❌ ERROR OCCURRED ❌ ❌ ❌")
        traceback.print_exc()
