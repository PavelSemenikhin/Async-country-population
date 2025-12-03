from bs4 import BeautifulSoup

from app.pydantic_models import CountryData


def extract_table(html: str):

    soup = BeautifulSoup(html, "lxml")

    table = soup.find("table", class_="wikitable")

    if not table:
        raise ValueError("Population table not found on page")
    return table


def parse_row(row):
    cells = row.find_all("td")
    if len(cells) < 3:
        return None

    country_a = cells[0].find("a")

    if country_a:
        country = country_a.get_text(strip=True)
    else:
        return None

    if country == "World":
        return None

    # population 2023
    population_raw = cells[2].get_text(strip=True).replace(",", "")

    if population_raw.isdigit():
        population = int(population_raw)
    else:
        population = 0

    region_a = cells[4].find("a")

    if region_a:
        region = region_a.get_text(strip=True)
    else:
        region = None

    return CountryData(
        country=country,
        population=population,
        region=region,
        source="wiki"
    )


def parse_population_table(html: str):
    table = extract_table(html)
    tbody = table.find("tbody")

    return [parsed for row in tbody.find_all("tr") if (parsed := parse_row(row))]
