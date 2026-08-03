"""
Pulls a random trending/searched GIF from Giphy.
Requires GIPHY_API_KEY — get a free one at https://developers.giphy.com/
"""
import random
import logging
import aiohttp

from config import GIPHY_API_KEY, GIF_SEARCH_TERMS

logger = logging.getLogger(__name__)


async def get_random_gif() -> dict | None:
    """
    Returns {"url": ..., "title": ...} or None if unavailable/failed.
    """
    if not GIPHY_API_KEY:
        logger.info("No GIPHY_API_KEY set — skipping GIF source.")
        return None

    term = random.choice(GIF_SEARCH_TERMS)
    url = "https://api.giphy.com/v1/gifs/search"
    params = {
        "api_key": GIPHY_API_KEY,
        "q": term,
        "limit": 25,
        "rating": "pg-13",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    logger.warning("Giphy fetch failed: HTTP %s", resp.status)
                    return None
                data = await resp.json()
    except Exception as e:
        logger.warning("Giphy fetch error: %s", e)
        return None

    results = data.get("data", [])
    if not results:
        return None

    choice = random.choice(results)
    gif_url = choice.get("images", {}).get("original", {}).get("url")
    if not gif_url:
        return None

    return {"url": gif_url, "title": choice.get("title") or term}
