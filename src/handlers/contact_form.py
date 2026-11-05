"""Contact form conversation handler."""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters,
)
from src.utils.config import config

NAME, EMAIL, MESSAGE = range(3)

async def start_contact_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    text = "✉️ <b>Send us a message</b>\n\nPlease enter your <b>Full Name</b>:\n\n<i>(Or type /cancel to abort)</i>"
    await query.edit_message_text(text, parse_mode=ParseMode.HTML)
    return NAME

async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['contact_name'] = update.message.text
    await update.message.reply_text("📧 Great! Now please enter your <b>Email Address</b>:", parse_mode=ParseMode.HTML)
    return EMAIL

async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    if "@" not in email or "." not in email:
        await update.message.reply_text("⚠️ That doesn't look like a valid email. Please try again:")
        return EMAIL
    context.user_data['contact_email'] = email
    await update.message.reply_text("📝 Finally, please type your <b>Message</b>:", parse_mode=ParseMode.HTML)
    return MESSAGE

async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    message_text = update.message.text
    name = context.user_data.get('contact_name')
    email = context.user_data.get('contact_email')
    user = update.effective_user
    admin_msg = (
        "📥 <b>New Contact Message</b>\n\n"
        f"👤 <b>Name:</b> {name}\n📧 <b>Email:</b> {email}\n"
        f"🆔 <b>Telegram:</b> @{user.username or 'None'} (ID: {user.id})\n\n"
        f"💬 <b>Message:</b>\n<i>{message_text}</i>"
    )
    for admin_id in config.ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode=ParseMode.HTML)
        except Exception: pass
    await update.message.reply_text("✅ <b>Message Sent!</b>\n\nThank you for reaching out.", parse_mode=ParseMode.HTML)
    context.user_data.clear()
    return ConversationHandler.END

async def cancel_contact_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("❌ Contact form cancelled. You can use the menu below.", parse_mode=ParseMode.HTML)
    context.user_data.clear()
    return ConversationHandler.END

# The fix is here: we add a catch-all MessageHandler to cancel the form if they click another menu button
contact_form_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(start_contact_form, pattern="^start_contact_form$")],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
        MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_contact_form),
        MessageHandler(filters.Regex("^🏠 Main Menu$"), cancel_contact_form),
        MessageHandler(filters.Regex("^🛠 Services$"), cancel_contact_form),
        MessageHandler(filters.Regex("^💼 Projects$"), cancel_contact_form),
        MessageHandler(filters.Regex("^🧠 Mr. Computer$"), cancel_contact_form),
        MessageHandler(filters.Regex("^🚀 Start Project$"), cancel_contact_form),
        MessageHandler(filters.Regex("^📺 Bahoush Media$"), cancel_contact_form),
        MessageHandler(filters.Regex("^ℹ️ About Us$"), cancel_contact_form),
        MessageHandler(filters.Regex("^📞 Contact$"), cancel_contact_form),
    ],
)
