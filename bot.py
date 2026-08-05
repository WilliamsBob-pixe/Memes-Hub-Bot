"""
Meme Hub Bot 😂
Posts a mix of Reddit memes, Giphy GIFs, and AI-generated jokes to a
Telegram chat/channel on a schedule. Also supports on-demand commands.

Setup:
    pip install -r requirements.txt
    export TELEGRAM_BOT_TOKEN="123456:ABC-your-bot-token"
    export TELEGRAM_CHAT_ID="@your_channel_or_chat_id"
    export GIPHY_API_KEY="..."          # optional
    export ANTHROPIC_API_KEY="..."      # optional
    python bot.py
"""
import asyncio
import logging
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import config
from sources.reddit_memes import get_random_meme
from sources.giphy_gifs import get_random_gif
from sources.ai_jokes import get_ai_joke

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("meme_hub_bot")


async def post_random_content(bot):
    """
    Picks a content type at random and posts it to the configured chat.
    Falls back to a joke if the chosen source has nothing available,
    so a scheduled post is never silently skipped.
    """
    content_type = random.choice(["meme", "gif", "joke"])

    if content_type == "meme":
        meme = await get_random_meme()
        if meme:
            caption = f"😂 {meme['title']}"
            await bot.send_photo(chat_id=config.CHAT_ID, photo=meme["url"], caption=caption)
            logger.info("Posted meme: %s", meme["title"])
            return
        content_type = "joke"  # fallback if reddit failed

    if content_type == "gif":
        gif = await get_random_gif()
        if gif:
            await bot.send_animation(chat_id=config.CHAT_ID, animation=gif["url"], caption=f"🎬 {gif['title']}")
            logger.info("Posted gif: %s", gif["title"])
            return
        content_type = "joke"  # fallback if giphy failed/unset

    joke = await get_ai_joke()
    await bot.send_message(chat_id=config.CHAT_ID, text=f"😂 {joke}")
    logger.info("Posted joke: %s", joke)


# ---------- On-demand commands ----------

async def cmd_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    meme = await get_random_meme()
    if meme:
        await update.message.reply_photo(photo=meme["url"], caption=f"😂 {meme['title']}")
    else:
        await update.message.reply_text("Couldn't fetch a meme right now — try again in a bit!")


async def cmd_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif = await get_random_gif()
    if gif:
        await update.message.reply_animation(animation=gif["url"], caption=f"🎬 {gif['title']}")
    else:
        await update.message.reply_text("GIF source isn't configured or is unavailable right now.")


async def cmd_joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = await get_ai_joke()
    await update.message.reply_text(f"😂 {joke}")


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Meme Hub Bot 😂\n"
        "I post memes, GIFs, and jokes on a schedule.\n\n"
        "Commands:\n"
        "/meme - get a random meme\n"
        "/gif - get a random GIF\n"
        "/joke - get an AI-generated joke"
    )


# ---------- Startup ----------

async def on_startup(app: Application):
    """Wire up the recurring scheduled post once the bot is running."""
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        post_random_content,
        "interval",
        hours=config.POST_INTERVAL_HOURS,
        args=[app.bot],
        next_run_time=None,  # first run after one interval; see README to post immediately on boot
    )
    scheduler.start()
    logger.info("Scheduler started: posting every %s hours to chat %s",
                config.POST_INTERVAL_HOURS, config.CHAT_ID)


def main():
    if not config.TELEGRAM_BOT_TOKEN or not config.CHAT_ID:
        raise SystemExit(
            "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID environment variables. "
            "See the top of bot.py for setup instructions."
        )
import telegram
print("=== NEW VERSION DEPLOYED ===", flush=True)
print("Telegram version:", telegram.__version__)
print("Telegram location:", telegram.__file__)

    app = Application.builder().token(config.TELEGRAM_BOT_TOKEN).post_init(on_startup).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("meme", cmd_meme))
    app.add_handler(CommandHandler("gif", cmd_gif))
    app.add_handler(CommandHandler("joke", cmd_joke))

    logger.info("Meme Hub Bot starting...")
    app.run_polling()


if __name__ == "__main__":
    main()
