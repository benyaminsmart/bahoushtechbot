"""Handlers for displaying services, projects, media, about, and contact."""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from src.content import SERVICES, PROJECTS, ABOUT, CONTACT
from src.keyboards.main_menu import services_inline_keyboard, projects_inline_keyboard
from src.utils.config import config


async def show_services_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "🛠 <b>My Services</b>\n\n"
        "Intelligent digital solutions engineered for the future.\n"
        "<i>Select a service to learn more:</i>"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=services_inline_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=services_inline_keyboard())


async def show_projects_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "💼 <b>My Projects</b>\n\n"
        "Explore our portfolio of intelligent platforms.\n"
        "<i>Select a project to see details:</i>"
    )
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=projects_inline_keyboard())
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=projects_inline_keyboard())


async def show_service_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    svc_id = query.data.replace("svc_", "")
    service = next((s for s in SERVICES if s["id"] == svc_id), None)
    
    if not service:
        await query.answer("Service not found.", show_alert=True)
        return

    tags = " • ".join([f"#{t.strip()}" for t in service["tags"]])
    text = (
        f"{service['icon']} <b>{service['title']}</b>\n\n"
        f"{service['short']}\n\n"
        f"<i>{service['details']}</i>\n\n"
        f"🏷 <code>{tags}</code>"
    )

    keyboard = [
        [InlineKeyboardButton("🚀 Request Consultation", callback_data="menu_form")],
        [InlineKeyboardButton("🌐 View on site", url=config.SITE_URL)],
        [InlineKeyboardButton("« Back to Services", callback_data="back_services")]
    ]

    await query.edit_message_text(text=text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))


async def show_project_detail(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    
    prj_id = query.data.replace("prj_", "")
    project = next((p for p in PROJECTS if p["id"] == prj_id), None)
    
    if not project:
        await query.answer("Project not found.", show_alert=True)
        return

    tags = " • ".join([f"#{t.strip()}" for t in project["tags"]])
    text = (
        f"{project['icon']} <b>{project['name']}</b> {project['status_icon']} <i>{project['status']}</i>\n\n"
        f"<b>{project['tagline']}</b>\n\n"
        f"{project['description']}\n\n"
        f"🏷 <code>{tags}</code>"
    )

    project_url = f"{config.SITE_URL}/{project['url']}"
    keyboard = [
        [InlineKeyboardButton("🌐 View on site", url=project_url)],
        [InlineKeyboardButton("« Back to Projects", callback_data="back_projects")]
    ]

    await query.edit_message_text(text=text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))


async def show_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📺 <b>BAHOUSH MEDIA</b>\n\n"
        "The media arm of Bahoush Tech — sharing visual stories, "
        "behind-the-scenes content, tech highlights, tutorials, and product demos.\n\n"
        "<b>Follow us and explore:</b>"
    )
    
    keyboard = [
        [
            InlineKeyboardButton("📸 Instagram", url=config.INSTAGRAM_URL),
            InlineKeyboardButton("💼 LinkedIn", url=config.LINKEDIN_URL)
        ],
        [InlineKeyboardButton("🌐 Website", url=config.SITE_URL)]
    ]
    
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        f"ℹ️ <b>About BAHOUSH TECH</b>\n\n"
        f"<i>“{ABOUT['tagline']}”</i>\n\n"
        f"{ABOUT['intro']}\n\n"
        f"<b>What we do:</b>\n"
    )
    
    for icon, title, desc in ABOUT['domains']:
        text += f"\n{icon} <b>{title}</b>\n{desc}\n"
        
    text += f"\n<i>{ABOUT['footer']}</i>"

    keyboard = [[InlineKeyboardButton("🌐 Visit Website", url=config.SITE_URL)]]

    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))


async def show_contact(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "📞 <b>Contact BAHOUSH TECH</b>\n\n"
        f"📧 <b>Email:</b> {CONTACT['email']}\n"
        f"📍 <b>Location:</b> {CONTACT['location']}\n"
        f"🌐 <b>Website:</b> {config.SITE_URL}\n\n"
        f"<i>{CONTACT['note']}</i>"
    )
    
    # Added the "Send a Message" button which triggers the conversation
    keyboard = [
        [InlineKeyboardButton("✉️ Send a Message", callback_data="start_contact_form")],
        [
            InlineKeyboardButton("📸 Instagram", url=config.INSTAGRAM_URL),
            InlineKeyboardButton("💼 LinkedIn", url=config.LINKEDIN_URL)
        ],
        [InlineKeyboardButton("🌐 Website", url=config.SITE_URL)]
    ]
    
    if update.message:
        await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
    elif update.callback_query:
        await update.callback_query.edit_message_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
