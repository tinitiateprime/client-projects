from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("purchase_order_line_source", "supply_chain", DATA_DIR, "purchase_order_line_source.zip")
