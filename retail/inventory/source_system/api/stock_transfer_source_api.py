from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("stock_transfer_source", "inventory", DATA_DIR, "stock_transfer_source.zip")
