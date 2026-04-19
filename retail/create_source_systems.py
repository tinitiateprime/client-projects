from __future__ import annotations

import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent


DOMAINS = {
    "customer_360": {
        "title": "Customer 360",
        "ddl": "customer_360_source_ingestion_sqlserver.sql",
        "generator": "customer_360_source_generators.py",
        "generated_dir": "generated_customer_360",
        "tables": [
            "pos_customer_360_source",
            "crm_customer_360_source",
            "csv_customer_360_source",
            "customer_360_landing",
        ],
        "formats": [
            "POS and CRM source files are generated as zipped Snappy parquet chunks.",
            "CSV upload source files are generated as zipped CSV.",
            "Parquet is chunked by row count; default is 250,000 rows per file.",
        ],
    },
    "inventory": {
        "title": "Inventory",
        "ddl": "inventory_source_ingestion_sqlserver.sql",
        "generator": "inventory_source_generators.py",
        "generated_dir": "generated_inventory_sources",
        "tables": [
            "inventory_product_source",
            "inventory_store_source",
            "inventory_warehouse_source",
            "store_inventory_source",
            "warehouse_inventory_source",
            "inventory_movement_source",
            "purchase_order_source",
            "purchase_order_line_source",
            "stock_transfer_source",
            "stock_transfer_line_source",
        ],
        "formats": [
            "Small master and business-event feeds are generated as zipped CSV.",
            "Large inventory snapshots and movements are generated as zipped Snappy parquet chunks.",
            "Parquet is chunked by row count; default is 250,000 rows per file.",
        ],
    },
    "supply_chain": {
        "title": "Supply Chain",
        "ddl": "supply_chain_source_ingestion_sqlserver.sql",
        "generator": "supply_chain_source_generators.py",
        "generated_dir": "generated_supply_chain_sources",
        "tables": [
            "supplier_source",
            "carrier_source",
            "supply_chain_warehouse_source",
            "purchase_order_source",
            "purchase_order_line_source",
            "shipment_source",
            "shipment_line_source",
            "receiving_event_source",
        ],
        "formats": [
            "Reference feeds and receiving events are generated as zipped CSV.",
            "High-volume purchase order and shipment feeds are generated as zipped Snappy parquet chunks.",
            "Parquet is chunked by row count; default is 250,000 rows per file.",
        ],
    },
    "sales": {
        "title": "Sales",
        "ddl": "sales_source_ingestion_sqlserver.sql",
        "generator": "sales_source_generators.py",
        "generated_dir": "generated_sales_sources",
        "tables": [
            "sales_calendar_source",
            "product_master_source",
            "store_master_source",
            "channel_master_source",
            "pos_txn_line_source",
            "ecom_order_line_source",
            "return_line_source",
            "promo_event_source",
            "sales_target_plan_source",
        ],
        "formats": [
            "Reference and lower-volume feeds are generated as zipped CSV.",
            "POS and ecommerce transaction feeds are generated as zipped Snappy parquet chunks.",
            "Parquet is chunked by row count; default is 250,000 rows per file.",
        ],
    },
}


FACTORY = '''from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any
from zipfile import ZipFile

from fastapi import FastAPI, HTTPException, Query


def _coerce(value: str) -> Any:
    if value == "":
        return None
    return value


def _read_csv_from_zip(zip_path: Path, limit: int) -> list[dict[str, Any]]:
    if not zip_path.exists():
        return []

    rows: list[dict[str, Any]] = []
    with ZipFile(zip_path) as archive:
        csv_names = [name for name in archive.namelist() if name.lower().endswith(".csv")]
        if not csv_names:
            return []
        with archive.open(csv_names[0]) as raw:
            text = (line.decode("utf-8") for line in raw)
            reader = csv.DictReader(text)
            for row in reader:
                rows.append({key: _coerce(value) for key, value in row.items()})
                if len(rows) >= limit:
                    break
    return rows


def create_table_api(table_name: str, domain_name: str, data_dir: Path, zip_name: str | None = None) -> FastAPI:
    app = FastAPI(title=f"{domain_name} {table_name} Source API")
    source_zip = data_dir / (zip_name or f"{table_name}.zip")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "table": table_name}

    @app.get(f"/{table_name}")
    def list_rows(limit: int = Query(default=100, ge=1, le=1000)) -> dict[str, Any]:
        rows = _read_csv_from_zip(source_zip, limit)
        if not rows:
            rows = [{"source_table": table_name, "source_status": "sample"}]
        return {"table": table_name, "count": len(rows), "rows": rows}

    @app.post(f"/{table_name}")
    def accept_row(row: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "accepted",
            "table": table_name,
            "row": row,
        }

    @app.get(f"/{table_name}/schema")
    def schema() -> dict[str, Any]:
        rows = _read_csv_from_zip(source_zip, 1)
        columns = list(rows[0].keys()) if rows else []
        return {"table": table_name, "columns": columns}

    @app.get(f"/{table_name}/sample-json")
    def sample_json() -> dict[str, Any]:
        sample_path = data_dir / f"{table_name}.sample.json"
        if sample_path.exists():
            return json.loads(sample_path.read_text(encoding="utf-8"))
        return {"table": table_name, "sample": {}}

    return app
'''


REQUIREMENTS = '''fastapi>=0.110
uvicorn[standard]>=0.27
'''


FTP_COMPOSE = '''services:
  source-ftp:
    image: fauria/vsftpd
    container_name: retail-source-ftp
    ports:
      - "2121:21"
      - "21100-21110:21100-21110"
    environment:
      FTP_USER: source_user
      FTP_PASS: source_pass
      PASV_ADDRESS: 127.0.0.1
      PASV_MIN_PORT: 21100
      PASV_MAX_PORT: 21110
    volumes:
      - ../generated:/home/vsftpd/source_user
'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def api_module(domain: str, table: str) -> str:
    zip_name = f'{table}.zip'
    return f'''from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("{table}", "{domain}", DATA_DIR, "{zip_name}")
'''


def domain_readme(domain: str, config: dict) -> str:
    tables = "\n".join(f"- `{table}`" for table in config["tables"])
    formats = "\n".join(f"- {item}" for item in config["formats"])
    return f'''# {config["title"]} Source System

This folder contains the source-system layer requested in `retail/data-process.md`.

## Contents

- `db/source_db_ddl.sql` - SQL Server source database DDL and source ingestion objects.
- `data_generators/{config["generator"]}` - source data generator for this domain.
- `api/` - one FastAPI module per source table plus a shared table API factory.
- `ftp/docker-compose.yml` - local FTP server for publishing generated source files.
- `generated/` - expected output location for generated CSV/parquet zip files.

## Source Tables

{tables}

## Generator Format

{formats}

Run a small sample:

```powershell
python .\\data_generators\\{config["generator"]} --output-dir .\\generated
```

Run a table API:

```powershell
pip install -r .\\api\\requirements.txt
uvicorn api.{config["tables"][0]}_api:app --reload --port 8000
```

Run the FTP server:

```powershell
docker compose -f .\\ftp\\docker-compose.yml up -d
```
'''


def generator_readme(domain: str, config: dict) -> str:
    return f'''# {config["title"]} Data Generators

The generator emits zipped source files for source-system ingestion. It supports CSV and Snappy parquet outputs.

Parquet files use the standard high-volume layout of multiple row chunks per zip. The default chunk size is 250,000 rows per parquet file and can be changed with `--parquet-rows-per-file`.

```powershell
python .\\{config["generator"]} --output-dir ..\\generated
```
'''


def ftp_readme() -> str:
    return '''# Source FTP Server

Local FTP endpoint for source-system file landing.

```powershell
docker compose up -d
```

Connection defaults:

- Host: `localhost`
- Port: `2121`
- User: `source_user`
- Password: `source_pass`

The FTP root maps to the sibling `generated` folder.
'''


def main() -> None:
    for domain, config in DOMAINS.items():
        domain_dir = ROOT / domain
        source_dir = domain_dir / "source_system"
        db_dir = source_dir / "db"
        gen_dir = source_dir / "data_generators"
        api_dir = source_dir / "api"
        ftp_dir = source_dir / "ftp"
        generated_dir = source_dir / "generated"

        for folder in [db_dir, gen_dir, api_dir, ftp_dir, generated_dir]:
            folder.mkdir(parents=True, exist_ok=True)

        shutil.copy2(domain_dir / config["ddl"], db_dir / "source_db_ddl.sql")
        shutil.copy2(domain_dir / config["generator"], gen_dir / config["generator"])
        if domain != "customer_360":
            shutil.copy2(ROOT / "source_zip_generator_utils.py", gen_dir / "source_zip_generator_utils.py")

        write(source_dir / "README.md", domain_readme(domain, config))
        write(gen_dir / "README.md", generator_readme(domain, config))
        write(api_dir / "table_api_factory.py", FACTORY)
        write(api_dir / "requirements.txt", REQUIREMENTS)
        write(api_dir / "__init__.py", "")
        for table in config["tables"]:
            write(api_dir / f"{table}_api.py", api_module(domain, table))
        write(ftp_dir / "docker-compose.yml", FTP_COMPOSE)
        write(ftp_dir / "README.md", ftp_readme())
        write(generated_dir / ".gitkeep", "")


if __name__ == "__main__":
    main()
