"""Keyboard builders for Bahoush Tech bot."""

from telegram import (
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from src.utils.config import config


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
