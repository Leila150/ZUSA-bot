import discord
from datetime import datetime

from config import COLOR_MAIN


# =========================
# EMBED HELPER
# =========================
def create_embed(title: str, description: str, color: int = COLOR_MAIN):
    return discord.Embed(
        title=title,
        description=description,
        color=color,
        timestamp=datetime.utcnow()
    )


# =========================
# SUCCESS EMBED
# =========================
def success_embed(message: str):
    return discord.Embed(
        title="✅ Success",
        description=message,
        color=0x57F287,
        timestamp=datetime.utcnow()
    )


# =========================
# ERROR EMBED
# =========================
def error_embed(message: str):
    return discord.Embed(
        title="❌ Error",
        description=message,
        color=0xED4245,
        timestamp=datetime.utcnow()
    )


# =========================
# WARNING EMBED
# =========================
def warn_embed(message: str):
    return discord.Embed(
        title="⚠️ Warning",
        description=message,
        color=0xFEE75C,
        timestamp=datetime.utcnow()
    )


# =========================
# CHECK: IS OWNER
# =========================
def is_owner(user_id: int):
    from config import OWNER_ID
    return user_id == OWNER_ID


# =========================
# FORMAT TIME
# =========================
def format_time(seconds: int):
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    if hours:
        return f"{hours}h {minutes}m {sec}s"
    elif minutes:
        return f"{minutes}m {sec}s"
    return f"{sec}s"


# =========================
# SIMPLE LOG PRINT
# =========================
def log(message: str):
    print(f"[BOT LOG] {datetime.utcnow()} - {message}")