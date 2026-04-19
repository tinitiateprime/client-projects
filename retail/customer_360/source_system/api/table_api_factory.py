from __future__ import annotations

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
