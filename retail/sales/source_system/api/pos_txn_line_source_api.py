from pathlib import Path

from .table_api_factory import create_table_api


DATA_DIR = Path(__file__).resolve().parents[1] / "generated"
app = create_table_api("pos_txn_line_source", "sales", DATA_DIR, "pos_txn_line_source.zip")
