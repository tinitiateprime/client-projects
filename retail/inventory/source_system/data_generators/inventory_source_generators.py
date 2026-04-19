import argparse
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from source_zip_generator_utils import make_rng, random_city_state, random_company, random_timestamp, write_csv_zip, write_parquet_zip


DEFAULT_PRODUCT_ROWS = 10_000
DEFAULT_STORE_ROWS = 3_000
DEFAULT_WAREHOUSE_ROWS = 500
DEFAULT_STORE_INVENTORY_ROWS = 1_000_000
DEFAULT_WAREHOUSE_INVENTORY_ROWS = 1_000_000
DEFAULT_INVENTORY_MOVEMENT_ROWS = 1_000_000
DEFAULT_PURCHASE_ORDER_MONTHS = 24
DEFAULT_PURCHASE_ORDERS_PER_MONTH = 100
DEFAULT_PURCHASE_ORDER_LINES_PER_MONTH = 10_000
DEFAULT_STOCK_TRANSFERS_PER_MONTH = 100
DEFAULT_STOCK_TRANSFER_LINES_PER_MONTH = 10_000
DEFAULT_PARQUET_ROWS_PER_FILE = 250_000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate zipped source files for Inventory.")
    parser.add_argument("--product-rows", type=int, default=DEFAULT_PRODUCT_ROWS)
    parser.add_argument("--store-rows", type=int, default=DEFAULT_STORE_ROWS)
    parser.add_argument("--warehouse-rows", type=int, default=DEFAULT_WAREHOUSE_ROWS)
    parser.add_argument("--store-inventory-rows", type=int, default=DEFAULT_STORE_INVENTORY_ROWS)
    parser.add_argument("--warehouse-inventory-rows", type=int, default=DEFAULT_WAREHOUSE_INVENTORY_ROWS)
    parser.add_argument("--inventory-movement-rows", type=int, default=DEFAULT_INVENTORY_MOVEMENT_ROWS)
    parser.add_argument("--purchase-order-months", type=int, default=DEFAULT_PURCHASE_ORDER_MONTHS)
    parser.add_argument("--purchase-orders-per-month", type=int, default=DEFAULT_PURCHASE_ORDERS_PER_MONTH)
    parser.add_argument("--purchase-order-lines-per-month", type=int, default=DEFAULT_PURCHASE_ORDER_LINES_PER_MONTH)
    parser.add_argument("--stock-transfers-per-month", type=int, default=DEFAULT_STOCK_TRANSFERS_PER_MONTH)
    parser.add_argument("--stock-transfer-lines-per-month", type=int, default=DEFAULT_STOCK_TRANSFER_LINES_PER_MONTH)
    parser.add_argument("--parquet-rows-per-file", type=int, default=DEFAULT_PARQUET_ROWS_PER_FILE)
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "generated_inventory_sources")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    product_rng = make_rng(21)
    store_rng = make_rng(22)
    warehouse_rng = make_rng(23)
    store_inventory_rng = make_rng(24)
    warehouse_inventory_rng = make_rng(25)
    movement_rng = make_rng(26)
    purchase_order_rng = make_rng(27)
    purchase_order_line_rng = make_rng(28)
    transfer_rng = make_rng(29)
    transfer_line_rng = make_rng(30)
    months = [
        (date.today().replace(day=1) - timedelta(days=30 * offset)).replace(day=1)
        for offset in reversed(range(args.purchase_order_months))
    ]

    def product_row(i: int) -> list:
        cost = round(product_rng.uniform(3, 200), 2)
        price = round(cost * product_rng.uniform(1.1, 2.8), 2)
        return [
            i,
            f"SKU-{i:08d}",
            f"Product {i}",
            product_rng.choice(["electronics", "grocery", "apparel", "home", "beauty"]),
            product_rng.choice(["Acme", "Northwind", "Contoso", "Fabrikam", "Globex"]),
            cost,
            price,
            1,
            random_timestamp(product_rng),
        ]

    def store_row(i: int) -> list:
        city, state_code = random_city_state(store_rng)
        return [
            i,
            f"STR-{i:05d}",
            f"Store {i}",
            city,
            state_code,
            "USA",
            1,
            random_timestamp(store_rng),
        ]

    def warehouse_row(i: int) -> list:
        city, state_code = random_city_state(warehouse_rng)
        return {
            "warehouse_id": i,
            "warehouse_code": f"WH-{i:04d}",
            "warehouse_name": f"Warehouse {i}",
            "city": city,
            "state_code": state_code,
            "country_code": "USA",
            "is_active": 1,
            "created_at": random_timestamp(warehouse_rng),
        }

    def store_inventory_row(i: int) -> dict:
        on_hand = store_inventory_rng.randint(0, 500)
        reserved = store_inventory_rng.randint(0, min(40, on_hand))
        return {
            "store_inventory_id": i,
            "store_id": store_inventory_rng.randint(1, args.store_rows),
            "product_id": store_inventory_rng.randint(1, args.product_rows),
            "on_hand_qty": on_hand,
            "reserved_qty": reserved,
            "safety_stock_qty": store_inventory_rng.randint(5, 80),
            "reorder_point_qty": store_inventory_rng.randint(10, 120),
            "updated_at": random_timestamp(store_inventory_rng),
        }

    def warehouse_inventory_row(i: int) -> dict:
        on_hand = warehouse_inventory_rng.randint(0, 5000)
        allocated = warehouse_inventory_rng.randint(0, min(700, on_hand))
        return {
            "warehouse_inventory_id": i,
            "warehouse_id": warehouse_inventory_rng.randint(1, args.warehouse_rows),
            "product_id": warehouse_inventory_rng.randint(1, args.product_rows),
            "on_hand": on_hand,
            "allocated": allocated,
            "in_transit_in_qty": warehouse_inventory_rng.randint(0, 300),
            "in_transit_out_qty": warehouse_inventory_rng.randint(0, 300),
            "safety_stock_qty": warehouse_inventory_rng.randint(50, 300),
            "reorder_point_qty": warehouse_inventory_rng.randint(100, 500),
            "updated_at": random_timestamp(warehouse_inventory_rng),
        }

    def movement_row(i: int) -> dict:
        movement_type = movement_rng.choice(["sale", "return", "transfer_in", "transfer_out", "receive_po", "adjustment"])
        return {
            "movement_id": i,
            "product_id": movement_rng.randint(1, args.product_rows),
            "movement_type": movement_type,
            "source_store_id": movement_rng.randint(1, args.store_rows) if movement_type in {"sale", "return", "transfer_out"} else None,
            "source_warehouse_id": movement_rng.randint(1, args.warehouse_rows) if movement_type in {"transfer_out", "receive_po", "adjustment"} else None,
            "target_store_id": movement_rng.randint(1, args.store_rows) if movement_type in {"return", "transfer_in"} else None,
            "target_warehouse_id": movement_rng.randint(1, args.warehouse_rows) if movement_type in {"transfer_in", "receive_po"} else None,
            "quantity": movement_rng.randint(1, 200),
            "reference_type": movement_rng.choice(["ops", "po", "transfer", "sale"]),
            "reference_id": f"REF-{i:09d}",
            "movement_ts": random_timestamp(movement_rng),
            "created_at": random_timestamp(movement_rng),
        }

    def purchase_order_row(i: int) -> list:
        month_value = months[(i - 1) // args.purchase_orders_per_month]
        order_date = month_value + timedelta(days=purchase_order_rng.randint(0, 27))
        expected_date = order_date + timedelta(days=purchase_order_rng.randint(2, 21))
        return [
            i,
            f"PO-{i:08d}",
            random_company(purchase_order_rng, "Supplier"),
            purchase_order_rng.randint(1, args.warehouse_rows),
            purchase_order_rng.choice(["created", "approved", "received", "closed"]),
            order_date.isoformat(),
            expected_date.isoformat(),
            random_timestamp(purchase_order_rng),
        ]

    def purchase_order_line_row(i: int) -> list:
        total_purchase_orders = args.purchase_order_months * args.purchase_orders_per_month
        return [
            i,
            purchase_order_line_rng.randint(1, total_purchase_orders),
            purchase_order_line_rng.randint(1, args.product_rows),
            purchase_order_line_rng.randint(10, 2000),
            purchase_order_line_rng.randint(0, 1500),
            round(purchase_order_line_rng.uniform(3, 200), 2),
        ]

    def stock_transfer_row(i: int) -> list:
        month_value = months[(i - 1) // args.stock_transfers_per_month]
        requested_date = month_value + timedelta(days=transfer_rng.randint(0, 27))
        shipped_date = requested_date + timedelta(days=transfer_rng.randint(1, 5))
        received_date = shipped_date + timedelta(days=transfer_rng.randint(1, 7))
        source_type = transfer_rng.choice(["store", "warehouse"])
        target_type = "warehouse" if source_type == "store" else "store"
        return [
            i,
            f"TR-{i:08d}",
            source_type,
            transfer_rng.randint(1, args.store_rows if source_type == "store" else args.warehouse_rows),
            target_type,
            transfer_rng.randint(1, args.warehouse_rows if target_type == "warehouse" else args.store_rows),
            transfer_rng.choice(["requested", "shipped", "received", "cancelled"]),
            requested_date.isoformat(),
            shipped_date.isoformat(),
            received_date.isoformat(),
            random_timestamp(transfer_rng),
        ]

    def stock_transfer_line_row(i: int) -> list:
        total_transfers = args.purchase_order_months * args.stock_transfers_per_month
        requested_qty = transfer_line_rng.randint(1, 200)
        shipped_qty = transfer_line_rng.randint(0, requested_qty)
        received_qty = transfer_line_rng.randint(0, shipped_qty)
        return [
            i,
            transfer_line_rng.randint(1, total_transfers),
            transfer_line_rng.randint(1, args.product_rows),
            requested_qty,
            shipped_qty,
            received_qty,
        ]

    write_csv_zip(
        args.output_dir,
        "product_source.zip",
        "inventory_product_source.csv",
        ["product_id", "sku", "product_name", "category", "brand", "unit_cost", "unit_price", "is_active", "created_at"],
        args.product_rows,
        product_row,
    )
    write_csv_zip(
        args.output_dir,
        "store_source.zip",
        "inventory_store_source.csv",
        ["store_id", "store_code", "store_name", "city", "state_code", "country_code", "is_active", "created_at"],
        args.store_rows,
        store_row,
    )
    write_parquet_zip(
        args.output_dir,
        "warehouse_source.zip",
        "warehouse_source",
        "warehouse_source",
        args.parquet_rows_per_file,
        args.warehouse_rows,
        warehouse_row,
    )
    write_parquet_zip(
        args.output_dir,
        "store_inventory_source.zip",
        "store_inventory_source",
        "store_inventory_source",
        args.parquet_rows_per_file,
        args.store_inventory_rows,
        store_inventory_row,
    )
    write_parquet_zip(
        args.output_dir,
        "warehouse_inventory_source.zip",
        "warehouse_inventory_source",
        "warehouse_inventory_source",
        args.parquet_rows_per_file,
        args.warehouse_inventory_rows,
        warehouse_inventory_row,
    )
    write_parquet_zip(
        args.output_dir,
        "inventory_movement_source.zip",
        "inventory_movement_source",
        "inventory_movement_source",
        args.parquet_rows_per_file,
        args.inventory_movement_rows,
        movement_row,
    )
    write_csv_zip(
        args.output_dir,
        "purchase_order_source.zip",
        "purchase_order_source.csv",
        ["po_id", "po_number", "supplier_name", "warehouse_id", "po_status", "order_date", "expected_date", "created_at"],
        args.purchase_order_months * args.purchase_orders_per_month,
        purchase_order_row,
    )
    write_csv_zip(
        args.output_dir,
        "purchase_order_line_source.zip",
        "purchase_order_line_source.csv",
        ["po_line_id", "po_id", "product_id", "ordered_qty", "received_qty", "unit_cost"],
        args.purchase_order_months * args.purchase_order_lines_per_month,
        purchase_order_line_row,
    )
    write_csv_zip(
        args.output_dir,
        "stock_transfer_source.zip",
        "stock_transfer_source.csv",
        ["transfer_id", "transfer_number", "source_type", "source_id", "target_type", "target_id", "transfer_status", "requested_date", "shipped_date", "received_date", "created_at"],
        args.purchase_order_months * args.stock_transfers_per_month,
        stock_transfer_row,
    )
    write_csv_zip(
        args.output_dir,
        "stock_transfer_line_source.zip",
        "stock_transfer_line_source.csv",
        ["transfer_line_id", "transfer_id", "product_id", "requested_qty", "shipped_qty", "received_qty"],
        args.purchase_order_months * args.stock_transfer_lines_per_month,
        stock_transfer_line_row,
    )


if __name__ == "__main__":
    main()
