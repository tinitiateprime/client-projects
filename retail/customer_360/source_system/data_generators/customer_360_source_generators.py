import argparse
import csv
import json
import random
import shutil
import tempfile
import time
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


DEFAULT_TOTAL_CUSTOMERS = 100_000
DEFAULT_POS_ROWS = 100_000
DEFAULT_CRM_ROWS = 20_000
DEFAULT_CSV_ROWS = 2_000
DEFAULT_PARQUET_ROWS_PER_FILE = 250_000
SEED = 42

FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael",
    "Linda", "William", "Elizabeth", "David", "Barbara", "Richard", "Susan",
    "Joseph", "Jessica", "Thomas", "Sarah", "Charles", "Karen",
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
    "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
]
CITIES = [
    ("Chicago", "IL", "60601"),
    ("Dallas", "TX", "75201"),
    ("Houston", "TX", "77001"),
    ("Phoenix", "AZ", "85001"),
    ("Seattle", "WA", "98101"),
    ("Atlanta", "GA", "30301"),
    ("Miami", "FL", "33101"),
    ("Denver", "CO", "80201"),
    ("Boston", "MA", "02101"),
    ("Nashville", "TN", "37201"),
]
GENDERS = ["male", "female", "non_binary", "unknown"]
PHONE_TYPES = ["mobile", "home", "work"]
ADDRESS_TYPES = ["home", "billing", "shipping"]
CHANNELS = ["store", "web", "app"]
PAYMENT_TYPES = ["card", "cash", "wallet"]
ORDER_STATUSES = ["completed", "refunded", "cancelled"]
INTERACTION_TYPES = ["page_view", "click", "email_open", "sms_click", "call"]
RECORD_TYPES = ["CUSTOMER", "CONTACT", "ADDRESS", "ORDER", "INTERACTION"]
SOURCE_NAMES = ["pos", "crm", "csv"]

SOURCE_COLUMNS = [
    "source_load_id",
    "batch_id",
    "record_source",
    "record_type",
    "source_file_name",
    "source_row_number",
    "source_record_id",
    "customer_id",
    "source_customer_id",
    "first_name",
    "middle_name",
    "last_name",
    "dob",
    "gender",
    "ssn",
    "email_address",
    "phone_number",
    "phone_type",
    "is_verified",
    "opt_in_marketing",
    "address_type",
    "address_line_1",
    "address_line_2",
    "city",
    "state_code",
    "postal_code",
    "country_code",
    "order_id",
    "channel",
    "payment_type",
    "status",
    "gross_amount",
    "discount_amount",
    "net_amount",
    "interaction_type",
    "campaign_id",
    "event_ts",
    "ingest_ts",
    "raw_payload",
]

class ChunkedParquetWriter:
    def __init__(self, output_dir: Path, prefix: str, rows_per_file: int):
        self.output_dir = output_dir
        self.prefix = prefix
        self.rows_per_file = rows_per_file
        self.buffer: list[dict] = []
        self.file_index = 1
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def write_row(self, row: dict) -> None:
        self.buffer.append(row)
        if len(self.buffer) >= self.rows_per_file:
            self.flush()

    def flush(self) -> None:
        if not self.buffer:
            return
        table = pa.Table.from_pylist(self.buffer)
        output_path = self.output_dir / f"{self.prefix}_part_{self.file_index:05d}.parquet"
        pq.write_table(table, output_path, compression="snappy")
        self.buffer.clear()
        self.file_index += 1

    def close(self) -> None:
        self.flush()


def random_date_of_birth(rng: random.Random) -> str:
    start = date(1940, 1, 1)
    end = date(2005, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=rng.randint(0, delta))).isoformat()


def random_timestamp(rng: random.Random, years_back: int = 3) -> str:
    end = datetime.utcnow()
    start = end - timedelta(days=365 * years_back)
    delta_seconds = int((end - start).total_seconds())
    ts = start + timedelta(seconds=rng.randint(0, delta_seconds))
    return ts.strftime("%Y-%m-%d %H:%M:%S")


def build_customer_pool(total_customers: int) -> list[dict]:
    rng = random.Random(SEED)
    customers = []
    for i in range(1, total_customers + 1):
        first = rng.choice(FIRST_NAMES)
        middle = rng.choice(FIRST_NAMES) if rng.random() < 0.45 else ""
        last = rng.choice(LAST_NAMES)
        city, state_code, postal_code = rng.choice(CITIES)
        customers.append({
            "customer_id": f"CUST{i:09d}",
            "source_customer_id": f"SRC{i:09d}",
            "first_name": first,
            "middle_name": middle,
            "last_name": last,
            "dob": random_date_of_birth(rng),
            "gender": rng.choice(GENDERS),
            "ssn": f"{rng.randint(100, 999)}-{rng.randint(10, 99)}-{rng.randint(1000, 9999)}",
            "email_address": f"{first.lower()}.{last.lower()}.{i}@example.com",
            "phone_number": f"{rng.randint(200, 999)}{rng.randint(200, 999)}{rng.randint(1000, 9999)}",
            "phone_type": rng.choice(PHONE_TYPES),
            "is_verified": int(rng.random() < 0.7),
            "opt_in_marketing": int(rng.random() < 0.8),
            "address_type": rng.choice(ADDRESS_TYPES),
            "address_line_1": f"{rng.randint(100, 9999)} {rng.choice(LAST_NAMES)} St",
            "address_line_2": f"Apt {rng.randint(1, 999)}" if rng.random() < 0.25 else "",
            "city": city,
            "state_code": state_code,
            "postal_code": postal_code,
            "country_code": "USA",
        })
    return customers


def build_source_row(
    rng: random.Random,
    source_name: str,
    source_row_number: int,
    customer: dict,
    source_file_name: str,
) -> dict:
    gross_amount = round(rng.uniform(10, 1500), 2)
    discount_amount = round(rng.uniform(0, gross_amount * 0.25), 2)
    record_type = rng.choice(RECORD_TYPES)
    source_record_id = f"{source_name[:3].upper()}-{source_row_number:09d}"
    raw_payload = json.dumps({
        "source": source_name.upper(),
        "record_type": record_type,
        "source_record_id": source_record_id,
    })
    return {
        "source_load_id": source_row_number,
        "batch_id": f"{source_name}_BATCH_{(source_row_number - 1) // 100000 + 1:03d}",
        "record_source": source_name.upper(),
        "record_type": record_type,
        "source_file_name": source_file_name,
        "source_row_number": source_row_number,
        "source_record_id": source_record_id,
        "customer_id": customer["customer_id"],
        "source_customer_id": customer["source_customer_id"],
        "first_name": customer["first_name"],
        "middle_name": customer["middle_name"],
        "last_name": customer["last_name"],
        "dob": customer["dob"],
        "gender": customer["gender"],
        "ssn": customer["ssn"],
        "email_address": customer["email_address"],
        "phone_number": customer["phone_number"],
        "phone_type": customer["phone_type"],
        "is_verified": customer["is_verified"],
        "opt_in_marketing": customer["opt_in_marketing"],
        "address_type": customer["address_type"],
        "address_line_1": customer["address_line_1"],
        "address_line_2": customer["address_line_2"],
        "city": customer["city"],
        "state_code": customer["state_code"],
        "postal_code": customer["postal_code"],
        "country_code": customer["country_code"],
        "order_id": f"ORD{source_row_number:09d}",
        "channel": rng.choice(CHANNELS),
        "payment_type": rng.choice(PAYMENT_TYPES),
        "status": rng.choice(ORDER_STATUSES),
        "gross_amount": f"{gross_amount:.2f}",
        "discount_amount": f"{discount_amount:.2f}",
        "net_amount": f"{(gross_amount - discount_amount):.2f}",
        "interaction_type": rng.choice(INTERACTION_TYPES),
        "campaign_id": f"CMP-{rng.randint(1, 99999):05d}",
        "event_ts": random_timestamp(rng, years_back=2),
        "ingest_ts": random_timestamp(rng, years_back=1),
        "raw_payload": raw_payload,
    }


def source_row_to_csv(row: dict) -> list:
    return [row[column] for column in SOURCE_COLUMNS]


def cleanup_path(path: Path) -> None:
    if path.is_dir():
        for _ in range(10):
            try:
                shutil.rmtree(path)
            except (PermissionError, OSError):
                time.sleep(0.2)
            if not path.exists():
                break
    elif path.exists():
        for _ in range(5):
            try:
                path.unlink()
                if not path.exists():
                    break
            except PermissionError:
                time.sleep(0.2)


def zip_directory(source_dir: Path, zip_path: Path) -> None:
    cleanup_path(zip_path)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_handle:
        for file_path in sorted(source_dir.rglob("*")):
            if file_path.is_file():
                zip_handle.write(file_path, arcname=file_path.relative_to(source_dir.parent))


def zip_file(source_file: Path, zip_path: Path) -> None:
    cleanup_path(zip_path)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zip_handle:
        zip_handle.write(source_file, arcname=source_file.name)


def generate_source_files(
    output_dir: Path,
    source_name: str,
    customers: list[dict],
    row_count: int,
    parquet_rows_per_file: int,
    seed_offset: int,
) -> None:
    rng = random.Random(SEED + seed_offset)
    with tempfile.TemporaryDirectory(prefix=f"{source_name}_customer_360_") as temp_dir_name:
        temp_dir = Path(temp_dir_name)

        if source_name in {"pos", "crm"}:
            parquet_dir = temp_dir / f"{source_name}_parquet"
            parquet_zip = output_dir / f"{source_name}_parquet.zip"
            parquet_writer = ChunkedParquetWriter(
                parquet_dir,
                source_name,
                parquet_rows_per_file,
            )
            source_file_name = f"{source_name}.parquet"

            for source_row_number in range(1, row_count + 1):
                customer = customers[rng.randrange(len(customers))]
                row = build_source_row(
                    rng=rng,
                    source_name=source_name,
                    source_row_number=source_row_number,
                    customer=customer,
                    source_file_name=source_file_name,
                )
                parquet_writer.write_row(row)

            parquet_writer.close()
            zip_directory(parquet_dir, parquet_zip)
            return

        csv_path = temp_dir / "csv_customer_360_source.csv"
        csv_zip = output_dir / "csv_customer_360_source.zip"

        with csv_path.open("w", newline="", encoding="utf-8") as source_handle:
            source_csv_writer = csv.writer(source_handle)
            source_csv_writer.writerow(SOURCE_COLUMNS)

            for source_row_number in range(1, row_count + 1):
                customer = customers[rng.randrange(len(customers))]
                row = build_source_row(
                    rng=rng,
                    source_name=source_name,
                    source_row_number=source_row_number,
                    customer=customer,
                    source_file_name=csv_path.name,
                )
                source_csv_writer.writerow(source_row_to_csv(row))

        zip_file(csv_path, csv_zip)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Customer 360 source CSV and Parquet files."
    )
    parser.add_argument(
        "--total-customers",
        type=int,
        default=DEFAULT_TOTAL_CUSTOMERS,
        help="Total unique customers across all sources. Default: 100000",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=None,
        help="Legacy option. If provided, applies the same row count to POS, CRM, and CSV.",
    )
    parser.add_argument(
        "--pos-rows",
        type=int,
        default=DEFAULT_POS_ROWS,
        help="Rows for POS source. Default: 100000",
    )
    parser.add_argument(
        "--crm-rows",
        type=int,
        default=DEFAULT_CRM_ROWS,
        help="Rows for CRM source. Default: 20000",
    )
    parser.add_argument(
        "--csv-rows",
        type=int,
        default=DEFAULT_CSV_ROWS,
        help="Rows for CSV source. Default: 2000",
    )
    parser.add_argument(
        "--parquet-rows-per-file",
        type=int,
        default=DEFAULT_PARQUET_ROWS_PER_FILE,
        help="Rows per Parquet file chunk. Default: 250000",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd() / "generated_customer_360",
        help="Directory for generated files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    if args.rows is not None:
        args.pos_rows = args.rows
        args.crm_rows = args.rows
        args.csv_rows = args.rows

    customers = build_customer_pool(args.total_customers)

    print(
        f"Generating {args.total_customers:,} total customers with "
        f"POS={args.pos_rows:,}, CRM={args.crm_rows:,}, CSV={args.csv_rows:,} ..."
    )

    source_row_counts = {
        "pos": args.pos_rows,
        "crm": args.crm_rows,
        "csv": args.csv_rows,
    }
    for seed_offset, source_name in enumerate(SOURCE_NAMES, start=1):
        generate_source_files(
            output_dir=args.output_dir,
            source_name=source_name,
            customers=customers,
            row_count=source_row_counts[source_name],
            parquet_rows_per_file=args.parquet_rows_per_file,
            seed_offset=seed_offset,
        )
        print(f"Wrote and zipped {source_name} source output")



if __name__ == "__main__":
    main()
