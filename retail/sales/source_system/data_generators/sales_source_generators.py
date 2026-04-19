import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from source_zip_generator_utils import (
    make_rng,
    random_city_state,
    random_date,
    random_timestamp,
    write_csv_zip,
    write_parquet_zip,
)


DEFAULT_DATE_YEARS = 50
DEFAULT_PRODUCT_ROWS = 10_000
DEFAULT_STORE_ROWS = 3_000
DEFAULT_CHANNEL_ROWS = 4
DEFAULT_SALES_YEARS = 2
DEFAULT_DAILY_SALES = 10_000
DEFAULT_DAILY_RETURNS = 1_000
DEFAULT_PROMO_EVENTS_PER_IMPORTANT_DAY = 2_000
DEFAULT_PARQUET_ROWS_PER_FILE = 250_000


def get_sales_date_range(years: int) -> list[date]:
    end_date = date.today()
    start_date = end_date - timedelta(days=(365 * years) - 1)
    return [start_date + timedelta(days=offset) for offset in range((end_date - start_date).days + 1)]


def get_calendar_date_range(years: int) -> list[date]:
    end_date = date.today()
    start_date = end_date - timedelta(days=(365 * years) - 1)
    return [start_date + timedelta(days=offset) for offset in range((end_date - start_date).days + 1)]


def important_dates_for_year(year_num: int) -> set[date]:
    thanksgiving = date(year_num, 11, 1)
    while thanksgiving.weekday() != 3:
        thanksgiving += timedelta(days=1)
    thanksgiving += timedelta(weeks=3)
    return {
        date(year_num, 1, 1),
        date(year_num, 2, 14),
        date(year_num, 5, 1),
        date(year_num, 7, 4),
        date(year_num, 9, 1),
        date(year_num, 11, 11),
        thanksgiving,
        thanksgiving + timedelta(days=1),
        thanksgiving + timedelta(days=4),
        date(year_num, 12, 24),
        date(year_num, 12, 25),
        date(year_num, 12, 31),
    }


def build_important_days(dates: list[date]) -> list[date]:
    important = set()
    for current_date in dates:
        important.update(important_dates_for_year(current_date.year))
    return sorted(day for day in important if day in set(dates))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate zipped source files for Sales.")
    parser.add_argument("--date-years", type=int, default=DEFAULT_DATE_YEARS)
    parser.add_argument("--product-rows", type=int, default=DEFAULT_PRODUCT_ROWS)
    parser.add_argument("--store-rows", type=int, default=DEFAULT_STORE_ROWS)
    parser.add_argument("--channel-rows", type=int, default=DEFAULT_CHANNEL_ROWS)
    parser.add_argument("--sales-years", type=int, default=DEFAULT_SALES_YEARS)
    parser.add_argument("--daily-sales", type=int, default=DEFAULT_DAILY_SALES)
    parser.add_argument("--daily-returns", type=int, default=DEFAULT_DAILY_RETURNS)
    parser.add_argument("--promo-events-per-important-day", type=int, default=DEFAULT_PROMO_EVENTS_PER_IMPORTANT_DAY)
    parser.add_argument("--parquet-rows-per-file", type=int, default=DEFAULT_PARQUET_ROWS_PER_FILE)
    parser.add_argument("--output-dir", type=Path, default=Path.cwd() / "generated_sales_sources")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    master_rng = make_rng(10)
    pos_rng = make_rng(11)
    ecom_rng = make_rng(12)
    returns_rng = make_rng(13)
    promo_rng = make_rng(14)
    target_rng = make_rng(15)
    channels = ["store", "web", "app", "marketplace"]
    calendar_dates = get_calendar_date_range(args.date_years)
    sales_dates = get_sales_date_range(args.sales_years)
    important_days = build_important_days(sales_dates)
    total_sales_rows = len(sales_dates) * args.daily_sales
    total_returns_rows = len(sales_dates) * args.daily_returns
    total_promo_rows = len(important_days) * args.promo_events_per_important_day
    pos_rows_total = int(total_sales_rows * 0.7)
    ecom_rows_total = total_sales_rows - pos_rows_total
    pos_rows_per_day = args.daily_sales * 7 // 10
    ecom_rows_per_day = args.daily_sales - pos_rows_per_day

    def date_row(i: int) -> list:
        current_date = calendar_dates[i - 1]
        return [
            int(current_date.strftime("%Y%m%d")),
            current_date.isoformat(),
            current_date.isoweekday(),
            current_date.month,
            ((current_date.month - 1) // 3) + 1,
            current_date.year,
        ]

    def product_row(i: int) -> list:
        return [
            i,
            f"SKU-{i:08d}",
            f"Product {i}",
            master_rng.choice(["electronics", "grocery", "apparel", "home", "beauty"]),
            master_rng.choice(["Acme", "Northwind", "Contoso", "Fabrikam", "Globex"]),
        ]

    def store_row(i: int) -> list:
        city, state_code = random_city_state(master_rng)
        return [
            i,
            f"STR-{i:05d}",
            f"Store {i}",
            city,
            state_code,
            "USA",
        ]

    def channel_row(i: int) -> list:
        channel_name = channels[(i - 1) % len(channels)]
        return [i, channel_name]

    def pos_row(i: int) -> dict:
        day_index = (i - 1) // pos_rows_per_day
        day_value = sales_dates[min(day_index, len(sales_dates) - 1)]
        city, state_code = random_city_state(pos_rng)
        txn_ts = datetime.combine(day_value, datetime.min.time()) + timedelta(
            seconds=pos_rng.randint(0, 86399)
        )
        gross_amt = round(pos_rng.uniform(10, 1200), 2)
        discount_amt = round(pos_rng.uniform(0, min(150, gross_amt * 0.30)), 2)
        return {
            "txn_line_id": f"POSL-{i:09d}",
            "order_id": f"POSO-{i:08d}",
            "sku": f"SKU-{pos_rng.randint(1, args.product_rows):08d}",
            "store_code": f"STR-{pos_rng.randint(1, args.store_rows):05d}",
            "city": city,
            "state_code": state_code,
            "qty": pos_rng.randint(1, 8),
            "gross_amt": gross_amt,
            "discount_amt": discount_amt,
            "txn_ts": txn_ts.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def ecom_row(i: int) -> dict:
        day_index = (i - 1) // ecom_rows_per_day
        day_value = sales_dates[min(day_index, len(sales_dates) - 1)]
        order_ts = datetime.combine(day_value, datetime.min.time()) + timedelta(
            seconds=ecom_rng.randint(0, 86399)
        )
        gross_amt = round(ecom_rng.uniform(10, 900), 2)
        discount_amt = round(ecom_rng.uniform(0, min(120, gross_amt * 0.25)), 2)
        taxable = max(gross_amt - discount_amt, 0)
        return {
            "order_line_id": f"ECOML-{i:09d}",
            "order_id": f"ECOMO-{i:08d}",
            "sku": f"SKU-{ecom_rng.randint(1, args.product_rows):08d}",
            "channel": ecom_rng.choice(channels[1:]),
            "qty": ecom_rng.randint(1, 6),
            "gross_amt": gross_amt,
            "discount_amt": discount_amt,
            "tax_amt": round(taxable * 0.08, 2),
            "order_ts": order_ts.strftime("%Y-%m-%d %H:%M:%S"),
        }

    def returns_row(i: int) -> list:
        day_index = (i - 1) // args.daily_returns
        day_value = sales_dates[min(day_index, len(sales_dates) - 1)]
        return_ts = datetime.combine(day_value, datetime.min.time()) + timedelta(
            seconds=returns_rng.randint(0, 86399)
        )
        return [
            f"RET-{i:09d}",
            f"ORDL-{returns_rng.randint(1, total_sales_rows):09d}",
            returns_rng.choice(["damaged", "wrong_item", "size_issue", "late_delivery", "customer_remorse"]),
            returns_rng.randint(1, 3),
            round(returns_rng.uniform(5, 300), 2),
            return_ts.strftime("%Y-%m-%d %H:%M:%S"),
        ]

    def promo_row(i: int) -> list:
        important_day = important_days[(i - 1) // args.promo_events_per_important_day]
        event_ts = datetime.combine(important_day, datetime.min.time()) + timedelta(
            seconds=promo_rng.randint(0, 86399)
        )
        return [
            f"PROMO-{i:08d}",
            f"ORD-{promo_rng.randint(1, total_sales_rows):08d}",
            f"PRM{promo_rng.randint(1, 9999):04d}",
            promo_rng.choice(["black_friday", "cyber_monday", "holiday", "seasonal"]),
            round(promo_rng.uniform(2, 80), 2),
            event_ts.strftime("%Y-%m-%d %H:%M:%S"),
        ]

    def target_row(i: int) -> list:
        target_date = sales_dates[(i - 1) % len(sales_dates)]
        date_key = int(target_date.strftime("%Y%m%d"))
        store_id = ((i - 1) % args.store_rows) + 1
        channel_id = (((i - 1) // args.store_rows) % len(channels)) + 1
        return [
            f"TGT-{i:08d}",
            date_key,
            store_id,
            channel_id,
            round(target_rng.uniform(5000, 125000), 2),
            target_rng.randint(100, 5000),
        ]

    write_csv_zip(
        args.output_dir,
        "date_source.zip",
        "sales_calendar.csv",
        ["date_key", "full_date", "day_of_week", "month_num", "quarter_num", "year_num"],
        len(calendar_dates),
        date_row,
    )
    write_csv_zip(
        args.output_dir,
        "product_source.zip",
        "product_master.csv",
        ["product_id", "sku", "product_name", "category", "brand"],
        args.product_rows,
        product_row,
    )
    write_csv_zip(
        args.output_dir,
        "store_source.zip",
        "store_master.csv",
        ["store_id", "store_code", "store_name", "city", "state_code", "country_code"],
        args.store_rows,
        store_row,
    )
    write_csv_zip(
        args.output_dir,
        "channel_source.zip",
        "channel_master.csv",
        ["channel_id", "channel_name"],
        args.channel_rows,
        channel_row,
    )

    write_parquet_zip(args.output_dir, "pos_parquet.zip", "pos_parquet", "pos", args.parquet_rows_per_file, pos_rows_total, pos_row)
    write_parquet_zip(args.output_dir, "ecom_parquet.zip", "ecom_parquet", "ecom", args.parquet_rows_per_file, ecom_rows_total, ecom_row)
    write_csv_zip(
        args.output_dir,
        "returns_source.zip",
        "return_line.csv",
        ["return_id", "order_line_id", "return_reason", "return_qty", "return_amount", "return_ts"],
        total_returns_rows,
        returns_row,
    )
    write_csv_zip(
        args.output_dir,
        "promo_source.zip",
        "promo_event.csv",
        ["promo_event_id", "order_id", "promo_code", "promo_channel", "discount_value", "event_ts"],
        total_promo_rows,
        promo_row,
    )
    write_csv_zip(
        args.output_dir,
        "sales_target_source.zip",
        "sales_target_plan.csv",
        ["target_id", "date_key", "store_id", "channel_id", "target_net_sales", "target_units"],
        len(sales_dates) * args.store_rows * len(channels),
        target_row,
    )


if __name__ == "__main__":
    main()
