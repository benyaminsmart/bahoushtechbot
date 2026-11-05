"""Mr. Computer AI chat handler."""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes, ConversationHandler, CommandHandler,
    MessageHandler, CallbackQueryHandler, filters,
)
from src.content import MR_COMPUTER
from src.services.ai_client import get_ai_response
from src.keyboards.main_menu import main_menu_reply_keyboard

CHATTING = 0

async def start_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.callback_query:
        await update.callback_query.answer()
        msg_target = update.callback_query.message
    else:
        msg_target = update.message
    if "ai_history" not in context.user_data:
        context.user_data["ai_history"] = [{"role": "system", "content": MR_COMPUTER["system_prompt"]}]
    text = f"🧠 <b>{MR_COMPUTER['name']}</b>\n<i>{MR_COMPUTER['title']}</i>\n\n{MR_COMPUTER['greeting']}\n\n💡 <i>Just type your message below, or type /reset to start over.</i>"
    keyboard = [[InlineKeyboardButton("🗑 Reset Chat", callback_data="ai_reset")]]
    await msg_target.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    await msg_target.reply_text("You are now chatting with Mr. Computer. (Type /end to close chat)", reply_markup=main_menu_reply_keyboard())
    return CHATTING

async def handle_ai_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_text = update.message.text
    history = context.user_data.get("ai_history", [])
    history.append({"role": "user", "content": user_text})
    if len(history) > 11: history = [history[0]] + history[-10:]
    context.user_data["ai_history"] = history
    await update.message.chat.send_action(action="typing")
    reply = await get_ai_response(history)
    history.append({"role": "assistant", "content": reply})
    context.user_data["ai_history"] = history
    await update.message.reply_text(reply)

async def reset_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    if query: await query.answer()
    context.user_data["ai_history"] = [{"role": "system", "content": MR_COMPUTER["system_prompt"]}]
    msg = "🗑 <b>Chat reset!</b>\n\n" + MR_COMPUTER["greeting"]
    if query: await query.edit_message_text(msg, parse_mode=ParseMode.HTML)
    else: await update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    return CHATTING

async def end_ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.pop("ai_history", None)
    await update.message.reply_text("👋 <b>Chat ended.</b>", parse_mode=ParseMode.HTML, reply_markup=main_menu_reply_keyboard())
    return ConversationHandler.END

mr_computer_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^🧠 Mr. Computer$"), start_ai_chat),
        CommandHandler("ai", start_ai_chat),
        CommandHandler("mrcomputer", start_ai_chat),
        CallbackQueryHandler(start_ai_chat, pattern="^menu_ai$")
    ],
    states={
        CHATTING: [
            MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^🏠 Main Menu$") & ~filters.Regex("^🛠 Services$") & ~filters.Regex("^💼 Projects$") & ~filters.Regex("^🚀 Start Project$") & ~filters.Regex("^📺 Bahoush Media$") & ~filters.Regex("^ℹ️ About Us$") & ~filters.Regex("^📞 Contact$"), handle_ai_message),
            CallbackQueryHandler(reset_ai_chat, pattern="^ai_reset$"),
            CommandHandler("reset", reset_ai_chat),
        ]
    },
    fallbacks=[
        CommandHandler("end", end_ai_chat),
        CommandHandler("cancel", end_ai_chat),
        MessageHandler(filters.Regex("^🏠 Main Menu$"), end_ai_chat),
        MessageHandler(filters.Regex("^🛠 Services$"), end_ai_chat),
        MessageHandler(filters.Regex("^💼 Projects$"), end_ai_chat),
        MessageHandler(filters.Regex("^🚀 Start Project$"), end_ai_chat),
        MessageHandler(filters.Regex("^📺 Bahoush Media$"), end_ai_chat),
        MessageHandler(filters.Regex("^ℹ️ About Us$"), end_ai_chat),
        MessageHandler(filters.Regex("^📞 Contact$"), end_ai_chat),
    ],
)
