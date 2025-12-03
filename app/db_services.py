from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db_models import Country
from app.pydantic_models import CountryData


class DatabaseService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert_many(self, rows: list[CountryData]):

        countries = [
            Country(
                country=row.country,
                population=row.population,
                region=row.region,
                source=row.source,
            )
            for row in rows
        ]

        try:
            self.session.add_all(countries)
            await self.session.commit()

        except Exception:
            await self.session.rollback()
            raise

    async def fetch_region_stats(self):

        ranked = (
            select(
                Country.region.label("region"),
                Country.country.label("country"),
                Country.population.label("population"),
                func.sum(Country.population).over(partition_by=Country.region).label("total_population"),
                func.first_value(Country.country)
                .over(partition_by=Country.region, order_by=Country.population.desc())
                .label("largest_country"),
                func.first_value(Country.population)
                .over(partition_by=Country.region, order_by=Country.population.desc())
                .label("largest_population"),
                func.first_value(Country.country)
                .over(partition_by=Country.region, order_by=Country.population.asc())
                .label("smallest_country"),
                func.first_value(Country.population)
                .over(partition_by=Country.region, order_by=Country.population.asc())
                .label("smallest_population"),
                )
            .where(Country.region.is_not(None))
            .cte("ranked")
        )

        stmt = (
            select(
                ranked.c.region,
                ranked.c.total_population,
                ranked.c.largest_country,
                ranked.c.largest_population,
                ranked.c.smallest_country,
                ranked.c.smallest_population,
            )
            .distinct(ranked.c.region)
            .order_by(ranked.c.region)
        )

        result = await self.session.execute(stmt)
        return result.all()

    async def clear(self):
        await self.session.execute(delete(Country))
        await self.session.commit()
