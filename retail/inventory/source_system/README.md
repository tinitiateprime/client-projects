# Inventory Source System

This folder contains the source-system layer requested in `retail/data-process.md`.

## Contents

- `db/source_db_ddl.sql` - SQL Server source database DDL and source ingestion objects.
- `data_generators/inventory_source_generators.py` - source data generator for this domain.
- `api/` - one FastAPI module per source table plus a shared table API factory.
- `ftp/docker-compose.yml` - local FTP server for publishing generated source files.
- `generated/` - expected output location for generated CSV/parquet zip files.

## Source Tables

- `inventory_product_source`
- `inventory_store_source`
- `inventory_warehouse_source`
- `store_inventory_source`
- `warehouse_inventory_source`
- `inventory_movement_source`
- `purchase_order_source`
- `purchase_order_line_source`
- `stock_transfer_source`
- `stock_transfer_line_source`

## Generator Format

- Small master and business-event feeds are generated as zipped CSV.
- Large inventory snapshots and movements are generated as zipped Snappy parquet chunks.
- Parquet is chunked by row count; default is 250,000 rows per file.

Run a small sample:

```powershell
python .\data_generators\inventory_source_generators.py --output-dir .\generated
```

Run a table API:

```powershell
pip install -r .\api\requirements.txt
uvicorn api.inventory_product_source_api:app --reload --port 8000
```

Run the FTP server:

```powershell
docker compose -f .\ftp\docker-compose.yml up -d
```
