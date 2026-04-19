# Sales Source System

This folder contains the source-system layer requested in `retail/data-process.md`.

## Contents

- `db/source_db_ddl.sql` - SQL Server source database DDL and source ingestion objects.
- `data_generators/sales_source_generators.py` - source data generator for this domain.
- `api/` - one FastAPI module per source table plus a shared table API factory.
- `ftp/docker-compose.yml` - local FTP server for publishing generated source files.
- `generated/` - expected output location for generated CSV/parquet zip files.

## Source Tables

- `sales_calendar_source`
- `product_master_source`
- `store_master_source`
- `channel_master_source`
- `pos_txn_line_source`
- `ecom_order_line_source`
- `return_line_source`
- `promo_event_source`
- `sales_target_plan_source`

## Generator Format

- Reference and lower-volume feeds are generated as zipped CSV.
- POS and ecommerce transaction feeds are generated as zipped Snappy parquet chunks.
- Parquet is chunked by row count; default is 250,000 rows per file.

Run a small sample:

```powershell
python .\data_generators\sales_source_generators.py --output-dir .\generated
```

Run a table API:

```powershell
pip install -r .\api\requirements.txt
uvicorn api.sales_calendar_source_api:app --reload --port 8000
```

Run the FTP server:

```powershell
docker compose -f .\ftp\docker-compose.yml up -d
```
