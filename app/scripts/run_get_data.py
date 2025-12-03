import asyncio
import logging

from app.data_fetcher import fetch_html
from app.db_services import DatabaseService
from app.db_config import init_db, AsyncSessionLocal, engine
from app.parser import parse_population_table


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    await init_db()

    try:
        html = await fetch_html()

        parsed = parse_population_table(html)

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
