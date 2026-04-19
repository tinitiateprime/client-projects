from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("sales_calendar_source", "sales", DATA_DIR, "sales_calendar_source.zip")
