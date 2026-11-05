"""SQLite database operations."""

import aiosqlite
from datetime import datetime
from src.utils.config import config
from src.utils.logger import log

async def init_db() -> None:
    """Create tables if they don't exist."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                request_type TEXT,
                content TEXT,
                created_at TEXT
            )
        """)
        await db.commit()
        log.info("Database initialized.")

async def add_user(user_id: int, username: str, first_name: str) -> None:
    """Add a user to the database if they don't exist."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, username, first_name, joined_at) VALUES (?, ?, ?, ?)",
            (user_id, username, first_name, datetime.now().isoformat())
        )
        await db.commit()

async def get_stats() -> dict:
    """Get total users and total requests."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute("SELECT COUNT(*) FROM users") as cursor:
            users_count = (await cursor.fetchone())[0]
        async with db.execute("SELECT COUNT(*) FROM requests") as cursor:
            reqs_count = (await cursor.fetchone())[0]
    return {"users": users_count, "requests": reqs_count}

async def get_all_user_ids() -> list[int]:
    """Get all user IDs for broadcasting."""
    async with aiosqlite.connect(config.DB_PATH) as db:
        async with db.execute("SELECT user_id FROM users") as cursor:
            rows = await cursor.fetchall()
    return [row[0] for row in rows]
