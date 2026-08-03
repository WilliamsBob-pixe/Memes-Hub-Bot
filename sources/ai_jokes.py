"""
Generates a short original joke using the Anthropic API.
Requires ANTHROPIC_API_KEY. Falls back to a static joke list if unset
or if the request fails, so the bot never has "nothing to post".
"""
import random
import logging
import aiohttp

from config import ANTHROPIC_API_KEY

logger = logging.getLogger(__name__)

FALLBACK_JOKES = [
    "I told my computer I needed a break, and now it won't stop sending me KitKats.",
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I'm on a seafood diet. I see food, and I eat it.",
    "Parallel lines have so much in common. It's a shame they'll never meet.",
    "I used to be a banker, but I lost interest.",
]

JOKE_STYLES = [
    "a short pun",
    "a one-liner about everyday life",
    "a silly dad joke",
    "an absurd one-liner",
    "a witty observational joke",
]


async def get_ai_joke() -> str:
    if not ANTHROPIC_API_KEY:
        logger.info("No ANTHROPIC_API_KEY set — using fallback joke.")
        return random.choice(FALLBACK_JOKES)

    style = random.choice(JOKE_STYLES)
    prompt = (
        f"Write {style}. One or two sentences max. "
        "No preamble, no quotation marks, just the joke itself."
    )

    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": ANTHROPIC_API_KEY,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-sonnet-4-6",
                    "max_tokens": 100,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=15,
            )
            if resp.status != 200:
                logger.warning("Anthropic API failed: HTTP %s", resp.status)
                return random.choice(FALLBACK_JOKES)
            data = await resp.json()
            text_blocks = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            joke = "\n".join(text_blocks).strip()
            return joke or random.choice(FALLBACK_JOKES)
    except Exception as e:
        logger.warning("Anthropic API error: %s", e)
        return random.choice(FALLBACK_JOKES)
