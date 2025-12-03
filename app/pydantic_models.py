from pydantic import BaseModel


class CountryData(BaseModel):
    country: str
    population: int
    region: str | None = None
    source: str = "wiki"
