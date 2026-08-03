"""
Pulls meme images from Reddit's public .json endpoints — no API key needed.
Filters out stickied posts, self-text posts, and videos (Telegram wants a
direct image URL for send_photo).
"""
import random
import logging
import aiohttp

from config import MEME_SUBREDDITS

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": "MemeHubBot/1.0 (by u/meme-hub-bot)"}
VALID_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")


async def get_random_meme() -> dict | None:
    """
    Returns {"url": ..., "title": ..., "permalink": ...} or None on failure.
    """
    subreddit = random.choice(MEME_SUBREDDITS)
    url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit=50"

    try:
        async with aiohttp.ClientSession(headers=HEADERS) as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    logger.warning("Reddit fetch failed: HTTP %s", resp.status)
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning("Reddit fetch error: %s", e)
        return None

    posts = data.get("data", {}).get("children", [])
    candidates = []
    for post in posts:
        p = post.get("data", {})
        if p.get("stickied"):
            continue
        image_url = p.get("url_overridden_by_dest") or p.get("url", "")
        if image_url.lower().endswith(VALID_EXTENSIONS):
            candidates.append({
                "url": image_url,
                "title": p.get("title", "Meme"),
                "permalink": f"https://reddit.com{p.get('permalink', '')}",
            })

    if not candidates:
        return None

    return random.choice(candidates)
