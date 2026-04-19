from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("pos_customer_360_source", "customer_360", DATA_DIR, "pos_customer_360_source.zip")
