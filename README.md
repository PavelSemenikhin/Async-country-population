# Async Country Population Parser

A fully asynchronous service for downloading, parsing, storing, and aggregating population data from multiple online sources.  
The project uses Docker Compose, PostgreSQL, aiohttp, SQLAlchemy (async), and class‑based architecture.

---

## Project Overview

This service consists of two independent Docker services:

### **get_data**
- Downloads HTML from a selected data source  
- Uses a parser class depending on `SOURCE`  
- Extracts country, population, and region  
- Saves raw (non‑aggregated) records into PostgreSQL  

### **print_data**
- Executes a **single SQL aggregation query**  
- Groups countries by region  
- Prints:
  - Region name  
  - Total population  
  - Largest country + population  
  - Smallest country + population  

---

## How to Run

### 1. Clone the repository

```
git clone https://github.com/PavelSemenikhin/Async-country-population
cd Async-country-population
```

### 2. Create your `.env` file

Copy the example:

```
cp .env.example .env
```



### 3. Run services

```
docker compose up get_data
docker compose up print_data
```

These are the **exact commands** used during verification.

---

## Environment Variables

Your `.env` file controls both the database and parser source.

### Database
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=countries
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://postgres:postgres@pg:5432/countries
```

### Data URLs
The project supports two sources:

```
WIKI_URL=https://en.wikipedia.org/w/index.php?title=List_of_countries_by_population_(United_Nations)&oldid=1215058959
STAT_URL=https://statisticstimes.com/demographics/countries-by-population.php
```

### Source Toggle
Choose the parser:

```
SOURCE=wiki
# or
SOURCE=stat_times
```

After modifying, simply run:

```
docker compose up get_data
docker compose up print_data
```

---

## Example Output

```
Region: Africa
Total population: 1515140850
Largest country: Nigeria
Largest population: 232679478
Smallest country: Saint Helena
Smallest population: 5237
```

---

## Architecture Highlights

- `BaseParser` — abstract parser class  
- `WikiParser` — Wikipedia parser  
- `StatParser` — StatisticsTimes parser  
- `DatabaseService` — async CRUD and aggregation  
- `run_get_data.py` — fetch + parse + save  
- `run_print_data.py` — SQL aggregation + print  
- Fully async stack  
- Easy to extend with new parsers  

---

## Notes

- All DB schema creation is done automatically on container startup  
- Data in DB is always raw (per country)  
- Aggregation always happens at read‑time via SQL  
- Docker Compose orchestrates DB + services automatically  

---
