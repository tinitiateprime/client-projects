import argparse
import bisect
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from source_zip_generator_utils import make_rng, random_city_state, random_company, write_csv_zip, write_parquet_zip


DEFAULT_SUPPLIER_ROWS = 2_000
DEFAULT_CARRIER_ROWS = 200
DEFAULT_WAREHOUSE_ROWS = 500
DEFAULT_PO_YEARS = 2
DEFAULT_PURCHASE_ORDERS_PER_DAY = 1_000
DEFAULT_MIN_PO_LINES = 2
DEFAULT_MAX_PO_LINES = 5
DEFAULT_MIN_SHIPMENTS_PER_DAY = 3
DEFAULT_MAX_SHIPMENTS_PER_DAY = 10
DEFAULT_MIN_SHIPMENT_LINES = 3
DEFAULT_MAX_SHIPMENT_LINES = 10
DEFAULT_PARQUET_ROWS_PER_FILE = 250_000


def get_date_range(years: int) -> list[date]:
    end_date = date.today()
    start_date = end_date - timedelta(days=(365 * years) - 1)
    return [start_date + timedelta(days=offset) for offset in range((end_date - start_date).days + 1)]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate zipped source files for Supply Chain.")
    parser.add_argument("--supplier-rows", type=int, default=DEFAULT_SUPPLIER_ROWS)
    parser.add_argument("--carrier-rows", type=int, default=DEFAULT_CARRIER_ROWS)
    parser.add_argument("--warehouse-rows", type=int, default=DEFAULT_WAREHOUSE_ROWS)
    parser.add_argument("--po-years", type=int, default=DEFAULT_PO_YEARS)
    parser.add_argument("--purchase-orders-per-day", type=int, default=DEFAULT_PURCHASE_ORDERS_PER_DAY)
    parser.add_argument("--min-po-lines", type=int, default=DEFAULT_MIN_PO_LINES)
    parser.add_argument("--max-po-lines", type=int, default=DEFAULT_MAX_PO_LINES)
    parser.add_argument("--min-shipments-per-day", type=int, default=DEFAULT_MIN_SHIPMENTS_PER_DAY)
    parser.add_argument("--max-shipments-per-day", type=int, default=DEFAULT_MAX_SHIPMENTS_PER_DAY)
    parser.add_argument("--min-shipment-lines", type=int, default=DEFAULT_MIN_SHIPMENT_LINES)
    parser.add_argument("--max-shipment-lines", type=int, default=DEFAULT_MAX_SHIPMENT_LINES)
    parser.add_argument("--parquet-rows-per-file", type=int, default=DEFAULT_PARQUET_ROWS_PER_FILE)
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "generated_supply_chain_sources")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    supplier_rng = make_rng(31)
    carrier_rng = make_rng(32)
    warehouse_rng = make_rng(33)
    po_rng = make_rng(34)
    po_line_rng = make_rng(35)
    shipment_rng = make_rng(36)
    shipment_line_rng = make_rng(37)
    receiving_rng = make_rng(38)
    dates = get_date_range(args.po_years)
    total_po_rows = len(dates) * args.purchase_orders_per_day
    po_line_counts = [po_line_rng.randint(args.min_po_lines, args.max_po_lines) for _ in range(total_po_rows)]
    total_po_line_rows = sum(po_line_counts)
    shipment_counts = [shipment_rng.randint(args.min_shipments_per_day, args.max_shipments_per_day) for _ in dates]
    total_shipment_rows = sum(shipment_counts)
    shipment_line_counts = [shipment_line_rng.randint(args.min_shipment_lines, args.max_shipment_lines) for _ in range(total_shipment_rows)]
    total_shipment_line_rows = sum(shipment_line_counts)

    def supplier_row(i: int) -> list:
        return [
            i,
            f"SUP-{i:06d}",
            random_company(supplier_rng, "Supplier"),
            "USA",
            supplier_rng.choice(["gold", "silver", "bronze"]),
            1,
        ]

    def carrier_row(i: int) -> list:
        return [
            i,
            f"CAR-{i:04d}",
            random_company(carrier_rng, "Carrier"),
            carrier_rng.choice(["standard", "expedited", "overnight"]),
        ]

    def warehouse_row(i: int) -> list:
        city, state_code = random_city_state(warehouse_rng)
        return [
            i,
            f"WH-{i:04d}",
            f"Warehouse {i}",
            city,
            state_code,
            "USA",
        ]

    def po_row(i: int) -> dict:
        day_value = dates[(i - 1) // args.purchase_orders_per_day]
        order_ts = datetime.combine(day_value, datetime.min.time()) + timedelta(seconds=po_rng.randint(0, 86399))
        expected_date = day_value + timedelta(days=po_rng.randint(2, 21))
        return {
            "po_id": i,
            "po_number": f"PO-{i:09d}",
            "supplier_id": po_rng.randint(1, args.supplier_rows),
            "warehouse_id": po_rng.randint(1, args.warehouse_rows),
            "po_status": po_rng.choice(["created", "approved", "shipped", "received", "closed"]),
            "order_date": day_value.isoformat(),
            "expected_date": expected_date.isoformat(),
        }

    po_line_end_offsets = []
    offset = 0
    for count in po_line_counts:
        offset += count
        po_line_end_offsets.append(offset)

    def po_line_row(i: int) -> dict:
        po_id = bisect.bisect_left(po_line_end_offsets, i) + 1
        return {
            "po_line_id": i,
            "po_id": po_id,
            "sku": f"SKU-{po_line_rng.randint(1, 10000):08d}",
            "ordered_qty": po_line_rng.randint(10, 2000),
            "unit_cost": round(po_line_rng.uniform(3, 200), 2),
        }

    shipment_offsets = []
    offset = 1
    for count in shipment_counts:
        shipment_offsets.append((offset, offset + count - 1))
        offset += count

    def shipment_row(i: int) -> dict:
        cumulative = 0
        day_index = 0
        for idx, count in enumerate(shipment_counts):
            cumulative += count
            if i <= cumulative:
                day_index = idx
                break
        day_value = dates[day_index]
        shipped_ts = datetime.combine(day_value, datetime.min.time()) + timedelta(seconds=shipment_rng.randint(0, 86399))
        eta_ts = shipped_ts + timedelta(days=shipment_rng.randint(1, 7))
        delivered_ts = eta_ts + timedelta(days=shipment_rng.randint(0, 3))
        return {
            "shipment_id": i,
            "shipment_number": f"SHP-{i:09d}",
            "po_id": shipment_rng.randint(1, total_po_rows),
            "carrier_id": shipment_rng.randint(1, args.carrier_rows),
            "shipment_status": shipment_rng.choice(["created", "in_transit", "delivered", "delayed"]),
            "shipped_ts": shipped_ts.strftime("%Y-%m-%d %H:%M:%S"),
            "eta_ts": eta_ts.strftime("%Y-%m-%d %H:%M:%S"),
            "delivered_ts": delivered_ts.strftime("%Y-%m-%d %H:%M:%S"),
        }

    shipment_line_end_offsets = []
    offset = 0
    for count in shipment_line_counts:
        offset += count
        shipment_line_end_offsets.append(offset)

    def shipment_line_row(i: int) -> dict:
        shipment_id = bisect.bisect_left(shipment_line_end_offsets, i) + 1
        shipped_qty = shipment_line_rng.randint(1, 500)
        damaged_qty = shipment_line_rng.randint(0, min(20, shipped_qty))
        return {
            "shipment_line_id": i,
            "shipment_id": shipment_id,
            "sku": f"SKU-{shipment_line_rng.randint(1, 10000):08d}",
            "shipped_qty": shipped_qty,
            "damaged_qty": damaged_qty,
        }

    def receiving_row(i: int) -> list:
        shipment_id = receiving_rng.randint(1, total_shipment_rows)
        received_qty = receiving_rng.randint(1, 500)
        return [
            i,
            shipment_id,
            receiving_rng.randint(1, args.warehouse_rows),
            f"SKU-{receiving_rng.randint(1, 10000):08d}",
            received_qty,
            (datetime.utcnow() - timedelta(days=receiving_rng.randint(0, 730))).strftime("%Y-%m-%d %H:%M:%S"),
            int(receiving_rng.random() < 0.15),
        ]

    write_csv_zip(
        args.output_dir,
        "supplier_source.zip",
        "supplier_source.csv",
        ["supplier_id", "supplier_code", "supplier_name", "country_code", "supplier_tier", "is_active"],
        args.supplier_rows,
        supplier_row,
    )
    write_csv_zip(
        args.output_dir,
        "carrier_source.zip",
        "carrier_source.csv",
        ["carrier_id", "carrier_code", "carrier_name", "service_level"],
        args.carrier_rows,
        carrier_row,
    )
    write_csv_zip(
        args.output_dir,
        "warehouse_source.zip",
        "supply_chain_warehouse_source.csv",
        ["warehouse_id", "warehouse_code", "warehouse_name", "city", "state_code", "country_code"],
        args.warehouse_rows,
        warehouse_row,
    )
    write_parquet_zip(args.output_dir, "purchase_order_source.zip", "purchase_order_source", "purchase_order_source", args.parquet_rows_per_file, total_po_rows, po_row)
    write_parquet_zip(args.output_dir, "purchase_order_line_source.zip", "purchase_order_line_source", "purchase_order_line_source", args.parquet_rows_per_file, total_po_line_rows, po_line_row)
    write_parquet_zip(args.output_dir, "shipment_source.zip", "shipment_source", "shipment_source", args.parquet_rows_per_file, total_shipment_rows, shipment_row)
    write_parquet_zip(args.output_dir, "shipment_line_source.zip", "shipment_line_source", "shipment_line_source", args.parquet_rows_per_file, total_shipment_line_rows, shipment_line_row)
    write_csv_zip(
        args.output_dir,
        "receiving_event_source.zip",
        "receiving_event_source.csv",
        ["receiving_event_id", "shipment_id", "warehouse_id", "sku", "received_qty", "received_ts", "is_partial"],
        total_shipment_line_rows,
        receiving_row,
    )


if __name__ == "__main__":
    main()
