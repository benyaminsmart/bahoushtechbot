"""Admin panel handlers."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from src.utils.config import config
from src.database.db import get_stats, get_all_user_ids

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show admin panel."""
    user_id = update.effective_user.id
    if user_id not in config.ADMIN_IDS:
        await update.message.reply_text("⛔ You are not authorized to use this command.")
        return

    stats = await get_stats()
    text = (
        "👨‍💼 <b>Admin Panel</b>\n\n"
        f"👥 <b>Total Users:</b> {stats['users']}\n"
        f"📥 <b>Total Requests:</b> {stats['requests']}\n\n"
        "Choose an action:"
    )
    
    keyboard = [
        [InlineKeyboardButton("📢 Broadcast Message", callback_data="admin_broadcast")]
    ]
    
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask admin for broadcast message."""
    query = update.callback_query
    await query.answer()
    
    context.user_data['broadcast_mode'] = True
    await query.edit_message_text(
        "📢 <b>Broadcast Mode</b>\n\n"
        "Please type the message you want to send to all users. (Or type /cancel to abort)",
        parse_mode=ParseMode.HTML
    )

async def execute_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the message to all users."""
    if not context.user_data.get('broadcast_mode'):
        return
        
    msg_text = update.message.text
    user_ids = await get_all_user_ids()
    
    success = 0
    fail = 0
    
    status_msg = await update.message.reply_text(f"⏳ Sending to {len(user_ids)} users...")
    
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=uid, text=msg_text)
            success += 1
        except Exception:
            fail += 1
            
    context.user_data['broadcast_mode'] = False
    await status_msg.edit_text(
        f"✅ <b>Broadcast Complete</b>\n\n"
        f"Successful: {success}\n"
        f"Failed: {fail}",
        parse_mode=ParseMode.HTML
    )
