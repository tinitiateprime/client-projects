from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("ecom_order_line_source", "sales", DATA_DIR, "ecom_order_line_source.zip")
