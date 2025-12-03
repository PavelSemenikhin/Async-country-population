from sqlalchemy import String, BigInteger, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Country(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(255), nullable=False)
    population: Mapped[int] = mapped_column(BigInteger, nullable=False)
    region: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source: Mapped[str] = mapped_column(
        String(255),
        default="wiki",
        server_default=text("'wiki'"),
    )
