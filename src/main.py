"""Bahoush Tech Bot — entry point."""

import traceback
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.handlers.start import start_command
from src.handlers.help import help_command
from src.handlers.details import (
    show_services_list,
    show_projects_list,
    show_service_detail,
    show_project_detail,
    show_media,
    show_about,
    show_contact,
)
from src.handlers.contact_form import contact_form_handler
from src.handlers.project_form import project_form_handler
from src.handlers.mr_computer import mr_computer_handler
from src.keyboards.main_menu import main_menu_reply_keyboard
from src.utils.config import config
from src.utils.logger import log


async def handle_menu_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages sent from the Reply Keyboard."""
    text = update.message.text
    
    if text == "🛠 Services":
        await show_services_list(update, context)
    elif text == "💼 Projects":
        await show_projects_list(update, context)
    elif text == "📺 Bahoush Media":
        await show_media(update, context)
    elif text == "ℹ️ About Us":
        await show_about(update, context)
    elif text == "📞 Contact":
        await show_contact(update, context)
    else:
        # If it's none of the above and not caught by conversations
        await update.message.reply_text(
            "🤖 I didn't understand that. Please use the menu below.",
            reply_markup=main_menu_reply_keyboard()
        )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard callbacks."""
    query = update.callback_query
    data = query.data
    
    if data.startswith("svc_"):
        await show_service_detail(update, context)
    elif data.startswith("prj_"):
        await show_project_detail(update, context)
    elif data == "back_services":
        await show_services_list(update, context)
    elif data == "back_projects":
        await show_projects_list(update, context)
    elif data == "ignore":
        await query.answer()
    elif data == "menu_main":
        await start_command(update, context)
    else:
        await query.answer()


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
    # 1. Add ConversationHandlers FIRST (so they take priority)
    app.add_handler(mr_computer_handler)
    app.add_handler(contact_form_handler)
    app.add_handler(project_form_handler)
    
    # 2. Add standard commands
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    
    # 3. Add text and callback handlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu_text))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_error_handler(error_handler)

    print("🚀 4. Bot is running! Go to Telegram and press /start")
    print("🛑 Press Ctrl+C to stop.\n")
    
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("\n❌ ❌ ❌ ERROR OCCURRED ❌ ❌ ❌")
        traceback.print_exc()
