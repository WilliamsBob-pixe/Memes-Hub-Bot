# Meme Hub Bot 😂

A Telegram bot that posts memes, GIFs, and jokes on a schedule, with
on-demand commands too.

## What it does

- **Scheduled posts**: every `POST_INTERVAL_HOURS` (default 3), it posts
  one random piece of content — a Reddit meme image, a Giphy GIF, or an
  AI-generated joke.
- **On-demand commands**:
  - `/meme` — random meme from Reddit
  - `/gif` — random GIF from Giphy
  - `/joke` — AI-generated joke
  - `/start` — shows the welcome message

## 1. Create your Telegram bot

1. Message [@BotFather](https://t.me/BotFather) on Telegram.
2. Send `/newbot` and follow the prompts to get a bot token.
3. Add the bot to your channel/group as an admin (needed to post), or
   just DM it directly for personal use.
4. Get your chat ID:
   - For a public channel, it's `@your_channel_username`.
   - For a private chat/group, send a message in it, then check
     `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` for the
     `chat.id` field.

## 2. Get optional API keys

- **Giphy** (for GIFs): free key at https://developers.giphy.com/
- **Anthropic** (for AI-generated jokes): key at https://console.anthropic.com/
  - If you skip this, the bot uses a small built-in fallback joke list.

If you skip Giphy or Anthropic, the bot still runs — it just leans more
on whichever sources are configured.

## 3. Install & configure

```bash
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN="123456:ABC-your-bot-token"
export TELEGRAM_CHAT_ID="@your_channel_or_chat_id"
export GIPHY_API_KEY="your_giphy_key"        # optional
export ANTHROPIC_API_KEY="your_anthropic_key" # optional
export POST_INTERVAL_HOURS="3"                # optional, defaults to 3
```

## 4. Run it

```bash
python bot.py
```

The bot will start polling for commands and schedule the recurring post.

## Notes on customization

- **Subreddits**: edit `MEME_SUBREDDITS` in `config.py`.
- **GIF search terms**: edit `GIF_SEARCH_TERMS` in `config.py`.
- **Post immediately on startup** (instead of waiting for the first
  interval to elapse): in `bot.py`, change the scheduler job's
  `next_run_time=None` to `next_run_time=datetime.now()` (add
  `from datetime import datetime` at the top).
- **Content mix weighting**: `post_random_content()` in `bot.py` uses
  `random.choice(["meme", "gif", "joke"])` — swap in `random.choices`
  with `weights=[...]` if you want memes to show up more often than
  jokes, for example.

## Deploying so it runs 24/7

This script uses polling, so it just needs to stay running somewhere:
- A small VPS (DigitalOcean, Linode, etc.) with `pm2` or a systemd
  service to keep it alive and auto-restart.
- A free-tier service like Railway or Fly.io.
- A Raspberry Pi or always-on home machine.

Avoid serverless/one-shot platforms (like a bare AWS Lambda) unless you
adapt the scheduling to an external cron trigger instead of
APScheduler, since polling bots need a long-running process.
