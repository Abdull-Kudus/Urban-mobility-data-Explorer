# Database Setup

## Requirements

- MySQL installed and running
- Python 3
- mysql-connector-python library

## Steps

### 1. Install Python library

```bash
pip install mysql-connector-python
```

### 2. Create your config file

Create a file called `db_config.py` inside the `database/` folder:

```python
DB_CONFIG = {
    "host":     "127.0.0.1",
    "user":     "root",
    "password": "yourpassword",
    "database": "urban_mobility"
}
```

Replace `yourpassword` with your actual MySQL password.

### 3. Download the raw data file

Download `yellow_tripdata_2019-01.csv` from the TLC website and place it inside the `data/` folder. This file is not in the repo because it is too large for GitHub.

### 4. Clean the raw data

```bash
python3 database/clean_data.py
```

This reads `data/yellow_tripdata_2019-01.csv`, removes invalid rows, computes derived features, and saves the cleaned file as `data/yellow_cleaned_tripdata.csv`.

### 5. Create the database and tables

```bash
mysql -u root -p --protocol=TCP --host=127.0.0.1 --port=3306 < database/schema.sql
```

This creates the `urban_mobility` database with all 7 tables, indexes, and seed data.

### 6. Insert the cleaned data

```bash
python3 database/insert_tripdata.py
```

This inserts all cleaned trip records into the `trips` table with all derived features.

### 7. Verify

```bash
mysql -u root -p --protocol=TCP --host=127.0.0.1 --port=3306 -e "USE urban_mobility; SHOW TABLES; SELECT COUNT(*) FROM trips;"
```

---

## For the Backend

The database is named `urban_mobility`. Connect using:

``
Host:     127.0.0.1
Port:      3306
User:      root
Password:  your local password
Database:  urban_mobility

Main table to query is `trips`. It joins to `taxi_zones`, `boroughs`, `vendors`, `rate_codes`, and `payment_types` via foreign keys. Example query:

```sql
SELECT t.trip_id, t.pickup_datetime, b.borough_name, t.fare_amount
FROM trips t
JOIN taxi_zones tz ON t.pickup_location_id = tz.location_id
JOIN boroughs b ON tz.borough_id = b.borough_id
LIMIT 10;
```

## Notes

- `db_config.py` is in `.gitignore` — create it locally with their own password
- Run everything from the project root folder, not inside the database folder
- If you get a duplicate key error, drop the database first and rerun the schema:

```bash
mysql -u root -p --protocol=TCP --host=127.0.0.1 --port=3306 -e "DROP DATABASE IF EXISTS urban_mobility;"
mysql -u root -p --protocol=TCP --host=127.0.0.1 --port=3306 < database/schema.sql
```

- `yellow_tripdata_2019-01.csv` and `yellow_cleaned_tripdata.csv` are in `.gitignore` and must be created locally
