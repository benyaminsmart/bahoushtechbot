"""Keyboard builders for Bahoush Tech bot."""

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from src.utils.config import config
from src.content import SERVICES, PROJECTS


def main_menu_reply_keyboard() -> ReplyKeyboardMarkup:
    """Main menu — as a persistent Reply Keyboard at the bottom."""
    keyboard = [
        [KeyboardButton("🛠 Services"), KeyboardButton("💼 Projects")],
        [KeyboardButton("🧠 Mr. Computer"), KeyboardButton("🚀 Start Project")],
        [KeyboardButton("📺 Bahoush Media"), KeyboardButton("ℹ️ About Us")],
        [KeyboardButton("📞 Contact")],
    ]
    return ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True,
        is_persistent=True,
        input_field_placeholder="Choose an option...",
    )


def services_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for 5 services."""
    keyboard = []
    for service in SERVICES:
        keyboard.append([
            InlineKeyboardButton(
                f"{service['icon']} {service['title']}", 
                callback_data=f"svc_{service['id']}"
            )
        ])
    return InlineKeyboardMarkup(keyboard)


def projects_inline_keyboard() -> InlineKeyboardMarkup:
    """Inline keyboard for the 4 main projects (excluding Media & AI)."""
    main_projects = ["platform-x", "word-smart", "bahoushguard", "staysync"]
    
    keyboard = []
    for project in PROJECTS:
        if project["id"] in main_projects:
            keyboard.append([
                InlineKeyboardButton(
                    f"{project['icon']} {project['name']} {project['status_icon']}", 
                    callback_data=f"prj_{project['id']}"
                )
            ])
    return InlineKeyboardMarkup(keyboard)
