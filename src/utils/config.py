"""Configuration loader — reads from .env via python-dotenv."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / ".env")


class Config:
    """Central config, sourced from environment variables."""

    # Telegram
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    ADMIN_IDS: list[int] = [
        int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
    ]

    # Groq AI
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
    GROQ_API_URL: str = os.getenv(
        "GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions"
    )

    # Brand
    BRAND: str = "BAHOUSH TECH"
    TAGLINE: str = "Turn Ideas Into Reality"

    # Links
    SITE_URL: str = os.getenv("SITE_URL", "https://bahoushtech.com")
    INSTAGRAM_URL: str = os.getenv("INSTAGRAM_URL", "https://instagram.com/bahoushtech")
    LINKEDIN_URL: str = os.getenv(
        "LINKEDIN_URL", "https://linkedin.com/company/bahoushtech"
    )
    CONTACT_EMAIL: str = os.getenv("CONTACT_EMAIL", "info@bahoushtech.com")
    PROJECT_FORM_URL: str = os.getenv(
        "PROJECT_FORM_URL", "https://bahoushtech.com/start-project.html"
    )

    # Paths
    DB_PATH: str = os.getenv("DB_PATH", "data/bot.db")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/bot.log")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Assets
    BANNER_PATH: Path = ROOT / "assets" / "images" / "banner.jpg"


    @classmethod
    def validate(cls) -> None:
        """Raise if required env vars are missing."""
        missing = []
        if not cls.BOT_TOKEN:
            missing.append("BOT_TOKEN")
        if not cls.ADMIN_IDS:
            missing.append("ADMIN_IDS")
        if not cls.GROQ_API_KEY:
            missing.append("GROQ_API_KEY")
        if missing:
            raise ValueError(
                f"❌ Missing required env vars: {', '.join(missing)}. "
                f"Check your .env file."
            )


config = Config()
