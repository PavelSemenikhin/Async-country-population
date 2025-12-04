import logging
import os

import aiohttp
import asyncio
from aiohttp import ClientError


logger = logging.getLogger(__name__)

WIKI_URL = os.getenv(
    "WIKI_URL",
    "https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959",
)


class RequestError(Exception):
    pass


async def fetch_html(url: str = WIKI_URL, timeout: int = 10) -> str:
    """
    Downloads HTML from the given URL asynchronously.
    """

    source = os.getenv("SOURCE", "wiki")

    if source == "wiki":
        url = os.getenv("WIKI_URL")

    elif source == "stat_times":
        url = os.getenv("STAT_URL")

    else:
        raise ValueError(f"Unknown SOURCE {source}")

    logger.info(f"Fetching HTML from {url}")

    headers = {"User-Agent": "Mozilla/5.0 (compatible; PopulationBot/1.0)"}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    logger.error(f"Unexpected status code: {response.status}")
                    raise RequestError(f"Unexpected status code: {response.status}")

                return await response.text()

    except (asyncio.TimeoutError, ClientError) as e:
        logger.error(f"Failed to fetch HTML: {e}")
        raise RequestError(f"Failed to fetch HTML: {e}")
