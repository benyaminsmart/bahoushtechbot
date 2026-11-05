"""Project Request (Start Project) multi-step form handler."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)

from src.content import PROJECT_FORM
from src.utils.config import config

# Define states for the conversation
NAME, EMAIL, SVC, PRODUCT, DELIVERY, BUDGET, DETAILS = range(7)
STEPS = PROJECT_FORM["steps"]
TOTAL_STEPS = len(STEPS)


def get_progress_bar(current: int) -> str:
    """Generate a visual progress bar (e.g., ▰▰▰▱▱▱▱)."""
    filled = "▰" * current
    empty = "▱" * (TOTAL_STEPS - current)
    return f"<code>{filled}{empty}</code>"


async def start_project_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Triggered when user clicks 'Start Project' or 'Request Consultation'."""
    # Clear previous data
    context.user_data.clear()
    
    # If triggered by callback (inline button), answer the callback
    if update.callback_query:
        await update.callback_query.answer()
        msg_target = update.callback_query.message
    else:
        msg_target = update.message

    # Step 1: Name
    text = (
        f"🚀 <b>{PROJECT_FORM['title']}</b>\n\n"
        f"{PROJECT_FORM['intro']}\n\n"
        f"<b>Step 1 of {TOTAL_STEPS}</b> {get_progress_bar(1)}\n\n"
        f"{STEPS[0]['question']}\n\n"
        "<i>(Or type /cancel to abort)</i>"
    )
    
    await msg_target.reply_text(text, parse_mode=ParseMode.HTML)
    return NAME


async def receive_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save name, ask for email."""
    context.user_data['form_name'] = update.message.text
    
    text = (
        f"<b>Step 2 of {TOTAL_STEPS}</b> {get_progress_bar(2)}\n\n"
        f"{STEPS[1]['question']}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)
    return EMAIL


async def receive_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save email, ask for service type (inline buttons)."""
    email = update.message.text
    if "@" not in email or "." not in email:
        await update.message.reply_text("⚠️ That doesn't look like a valid email. Please try again:")
        return EMAIL
        
    context.user_data['form_email'] = email
    
    # Build inline keyboard for service type
    keyboard = []
    for opt in STEPS[2]['options']:
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"frm_svc_{opt}")])
    keyboard.append([InlineKeyboardButton("✖ Cancel", callback_data="frm_cancel")])
    
    text = (
        f"<b>Step 3 of {TOTAL_STEPS}</b> {get_progress_bar(3)}\n\n"
        f"{STEPS[2]['question']}"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    return SVC


async def receive_svc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save service, ask for product type."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "frm_cancel":
        return await cancel_form(update, context)
        
    svc_choice = query.data.replace("frm_svc_", "")
    context.user_data['form_svc'] = svc_choice

    keyboard = []
    for opt in STEPS[3]['options']:
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"frm_prd_{opt}")])
        
    text = (
        f"<b>Step 4 of {TOTAL_STEPS}</b> {get_progress_bar(4)}\n\n"
        f"{STEPS[3]['question']}"
    )
    await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    return PRODUCT


async def receive_product(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save product type, ask for delivery method."""
    query = update.callback_query
    await query.answer()
    
    prd_choice = query.data.replace("frm_prd_", "")
    context.user_data['form_prd'] = prd_choice

    keyboard = []
    for opt in STEPS[4]['options']:
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"frm_dlv_{opt}")])
        
    text = (
        f"<b>Step 5 of {TOTAL_STEPS}</b> {get_progress_bar(5)}\n\n"
        f"{STEPS[4]['question']}"
    )
    await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    return DELIVERY


async def receive_delivery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save delivery, ask for budget."""
    query = update.callback_query
    await query.answer()
    
    dlv_choice = query.data.replace("frm_dlv_", "")
    context.user_data['form_dlv'] = dlv_choice

    keyboard = []
    for opt in STEPS[5]['options']:
        keyboard.append([InlineKeyboardButton(opt, callback_data=f"frm_bgt_{opt}")])
        
    text = (
        f"<b>Step 6 of {TOTAL_STEPS}</b> {get_progress_bar(6)}\n\n"
        f"{STEPS[5]['question']}"
    )
    await query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    return BUDGET


async def receive_budget(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save budget, ask for extra details."""
    query = update.callback_query
    await query.answer()
    
    bgt_choice = query.data.replace("frm_bgt_", "")
    context.user_data['form_bgt'] = bgt_choice

    text = (
        f"<b>Step 7 of {TOTAL_STEPS}</b> {get_progress_bar(7)}\n\n"
        f"{STEPS[6]['question']}"
    )
    await query.edit_message_text(text, parse_mode=ParseMode.HTML)
    return DETAILS


async def receive_details(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Save details and send to admin."""
    details = update.message.text
    if details.strip().lower() == "/skip":
        details = "None provided"
        
    context.user_data['form_details'] = details
    user = update.effective_user

    # Format the message for admin
    admin_msg = (
        "📥 <b>New Project Request</b>\n\n"
        f"👤 <b>Name:</b> {context.user_data.get('form_name')}\n"
        f"📧 <b>Email:</b> {context.user_data.get('form_email')}\n"
        f"🆔 <b>Telegram:</b> @{user.username or 'None'} (ID: {user.id})\n\n"
        f"🎯 <b>Service Type:</b> {context.user_data.get('form_svc')}\n"
        f"📦 <b>Product Type:</b> {context.user_data.get('form_prd')}\n"
        f"🚀 <b>Delivery:</b> {context.user_data.get('form_dlv')}\n"
        f"💰 <b>Budget:</b> {context.user_data.get('form_bgt')}\n\n"
        f"📝 <b>Details:</b>\n<i>{context.user_data.get('form_details')}</i>"
    )

    # Send to all admins
    for admin_id in config.ADMIN_IDS:
        try:
            await context.bot.send_message(chat_id=admin_id, text=admin_msg, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"Failed to send to admin {admin_id}: {e}")

    # Confirm to user
    await update.message.reply_text(
        PROJECT_FORM['success'],
        parse_mode=ParseMode.HTML
    )
    
    context.user_data.clear()
    return ConversationHandler.END


async def cancel_form(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the project form."""
    msg = "❌ Project form cancelled. You can use the menu below to navigate."
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(msg)
    else:
        await update.message.reply_text(msg)
    context.user_data.clear()
    return ConversationHandler.END


# The ConversationHandler object for the Project Form
project_form_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("^🚀 Start Project$"), start_project_form),
        CallbackQueryHandler(start_project_form, pattern="^menu_form$")
    ],
    states={
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_name)],
        EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_email)],
        SVC: [CallbackQueryHandler(receive_svc, pattern="^frm_")],
        PRODUCT: [CallbackQueryHandler(receive_product, pattern="^frm_prd_")],
        DELIVERY: [CallbackQueryHandler(receive_delivery, pattern="^frm_dlv_")],
        BUDGET: [CallbackQueryHandler(receive_budget, pattern="^frm_bgt_")],
        DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_details)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel_form),
        CallbackQueryHandler(cancel_form, pattern="^frm_cancel$")
    ],
)
