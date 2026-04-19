from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("customer_360_landing", "customer_360", DATA_DIR, "customer_360_landing.zip")
