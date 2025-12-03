import asyncio
import logging

from app.db_services import DatabaseService
from app.db_config import AsyncSessionLocal, engine


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)


async def main():
    async with AsyncSessionLocal() as session:
        service = DatabaseService(session)
        rows = await service.fetch_region_stats()

        logger.info(f"Fetched {len(rows)} region statistics entries")

        for row in rows:
            data = row._mapping

            logger.info("=====================================")
            logger.info(f"Region:               {data['region']}")
            logger.info("-------------------------------------")
            logger.info(f"Total population:     {data['total_population']}")
            logger.info(f"Largest country:      {data['largest_country']}")
            logger.info(f"Largest population:   {data['largest_population']}")
            logger.info(f"Smallest country:     {data['smallest_country']}")
            logger.info(f"Smallest population:  {data['smallest_population']}")
            logger.info("=====================================\n")

    await engine.dispose()
    logger.info("Engine disposed. Shutdown complete.")


if __name__ == "__main__":
    asyncio.run(main())
