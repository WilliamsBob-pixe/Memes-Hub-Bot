"""
Configuration for Meme Hub Bot.
All secrets are loaded from environment variables — never hardcode keys here.
"""
import os

# --- Required ---
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")  # channel/group/user to post to

# --- Optional (feature degrades gracefully if missing) ---
GIPHY_API_KEY = os.environ.get("GIPHY_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# --- Behavior ---
POST_INTERVAL_HOURS = float(os.environ.get("POST_INTERVAL_HOURS", "3"))

# Subreddits to pull memes from (public JSON endpoints, no auth required)
MEME_SUBREDDITS = [
    "memes",
    "dankmemes",
    "wholesomememes",
    "ProgrammerHumor",
]

# Giphy search terms to rotate through for variety
GIF_SEARCH_TERMS = [
    "funny", "lol", "reaction", "cats", "fail", "monday mood",
]
