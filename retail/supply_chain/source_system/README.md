# Supply Chain Source System

This folder contains the source-system layer requested in `retail/data-process.md`.

## Contents

- `db/source_db_ddl.sql` - SQL Server source database DDL and source ingestion objects.
- `data_generators/supply_chain_source_generators.py` - source data generator for this domain.
- `api/` - one FastAPI module per source table plus a shared table API factory.
- `ftp/docker-compose.yml` - local FTP server for publishing generated source files.
- `generated/` - expected output location for generated CSV/parquet zip files.

## Source Tables

- `supplier_source`
- `carrier_source`
- `supply_chain_warehouse_source`
- `purchase_order_source`
- `purchase_order_line_source`
- `shipment_source`
- `shipment_line_source`
- `receiving_event_source`

## Generator Format

- Reference feeds and receiving events are generated as zipped CSV.
- High-volume purchase order and shipment feeds are generated as zipped Snappy parquet chunks.
- Parquet is chunked by row count; default is 250,000 rows per file.

Run a small sample:

```powershell
python .\data_generators\supply_chain_source_generators.py --output-dir .\generated
```

Run a table API:

```powershell
pip install -r .\api\requirements.txt
uvicorn api.supplier_source_api:app --reload --port 8000
```

Run the FTP server:

```powershell
docker compose -f .\ftp\docker-compose.yml up -d
```
