# Customer 360 Source System

This folder contains the source-system layer requested in `retail/data-process.md`.

## Contents

- `db/source_db_ddl.sql` - SQL Server source database DDL and source ingestion objects.
- `data_generators/customer_360_source_generators.py` - source data generator for this domain.
- `api/` - one FastAPI module per source table plus a shared table API factory.
- `ftp/docker-compose.yml` - local FTP server for publishing generated source files.
- `generated/` - expected output location for generated CSV/parquet zip files.

## Source Tables

- `pos_customer_360_source`
- `crm_customer_360_source`
- `csv_customer_360_source`
- `customer_360_landing`

## Generator Format

- POS and CRM source files are generated as zipped Snappy parquet chunks.
- CSV upload source files are generated as zipped CSV.
- Parquet is chunked by row count; default is 250,000 rows per file.

Run a small sample:

```powershell
python .\data_generators\customer_360_source_generators.py --output-dir .\generated
```

Run a table API:

```powershell
pip install -r .\api\requirements.txt
uvicorn api.pos_customer_360_source_api:app --reload --port 8000
```

Run the FTP server:

```powershell
docker compose -f .\ftp\docker-compose.yml up -d
```
