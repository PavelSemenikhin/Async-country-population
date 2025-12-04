from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from app.pydantic_models import CountryData


class BaseParser(ABC):

    source: str = "unknown"

    @abstractmethod
    def parse(self, html: str) -> list[CountryData]:
        pass


class WikiParser(BaseParser):

    source = "wiki"

    @staticmethod
    def extract_table(html: str):
        soup = BeautifulSoup(html, "lxml")

        table = soup.find("table", class_="wikitable")
        if not table:
            raise ValueError("Population table not found on page")

        return table

    def parse_row(self, row):
        cells = row.find_all("td")
        if len(cells) < 3:
            return None

        country_a = cells[0].find("a")
        if not country_a:
            return None

        country = country_a.get_text(strip=True)

        if country == "World":
            return None

        population_raw = cells[2].get_text(strip=True).replace(",", "")
        population = int(population_raw) if population_raw.isdigit() else 0

        region_a = cells[4].find("a")
        region = region_a.get_text(strip=True) if region_a else None

        return CountryData(
            country=country,
            population=population,
            region=region,
            source=self.source,
        )

    def parse(self, html: str) -> list[CountryData]:
        table = self.extract_table(html)
        tbody = table.find("tbody")

        parsed_rows = []

        for row in tbody.find_all("tr"):
            item = self.parse_row(row)
            if item:
                parsed_rows.append(item)

        return parsed_rows


class StatParser(BaseParser):

    source = "stat_times"

    @staticmethod
    def extract_table(html: str):
        soup = BeautifulSoup(html, "lxml")

        table = soup.find("table", id="table_id")
        if not table:
            raise ValueError("StatisticsTimes table not found on page")

        return table

    def parse_row(self, row):
        cells = row.find_all("td")
        if len(cells) < 9:
            return None

        country = cells[0].get_text(strip=True)
        if not country:
            return None

        population_raw = cells[1].get_text(strip=True).replace(",", "")
        try:
            population = int(population_raw)
        except ValueError:
            return None

        region = cells[8].get_text(strip=True)
        region = region if region else None

        return CountryData(
            country=country, population=population, region=region, source=self.source
        )

    def parse(self, html: str) -> list[CountryData]:
        table = self.extract_table(html)
        tbody = table.find("tbody")

        parsed_rows = []

        for row in tbody.find_all("tr"):
            item = self.parse_row(row)
            if item:
                parsed_rows.append(item)

        return parsed_rows
