import aiohttp
import asyncio
from aiohttp import ClientError


class RequestError(Exception):
    pass


async def fetch_html(url: str, timeout: int = 10) -> str:
    """
    Downloads HTML from the given URL asynchronously.
    """

    headers = {"User-Agent": "Mozilla/5.0 (compatible; PopulationBot/1.0)"}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    raise RequestError(f"Unexpected status code: {response.status}")

                return await response.text()

    except (asyncio.TimeoutError, ClientError) as e:
        raise RequestError(f"Failed to fetch HTML: {e}")
