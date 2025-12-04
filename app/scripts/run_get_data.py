import os
import logging
import asyncio

from app.data_fetcher import fetch_html
from app.db_services import DatabaseService
from app.db_config import init_db, AsyncSessionLocal, engine

from app.parser import WikiParser, StatParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    await init_db()

    try:
        html = await fetch_html()

        source = os.getenv("SOURCE", "wiki")

        if source == "wiki":
            parser = WikiParser()

        elif source == "stat_times":
            parser = StatParser()

        else:
            raise ValueError(
                f"Unknown source = {source} please choose from wiki or stat_times."
            )

        parsed = parser.parse(html)

        async with AsyncSessionLocal() as session:
            service = DatabaseService(session)

            await service.clear()
            await service.insert_many(parsed)

        logger.info("DATA INSERTED SUCCESSFULLY")
        logger.info(f"Inserted {len(parsed)} rows into DB")

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
