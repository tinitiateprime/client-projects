import csv
import random
import tempfile
import time
import zipfile
from datetime import date, datetime, timedelta
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq


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
    ("Chicago", "IL"),
    ("Dallas", "TX"),
    ("Houston", "TX"),
    ("Phoenix", "AZ"),
    ("Seattle", "WA"),
    ("Atlanta", "GA"),
    ("Miami", "FL"),
    ("Denver", "CO"),
    ("Boston", "MA"),
    ("Nashville", "TN"),
]


class ChunkedParquetWriter:
    def __init__(self, output_dir: Path, prefix: str, rows_per_file: int):
        self.output_dir = output_dir
        self.prefix = prefix
        self.rows_per_file = rows_per_file
        self.buffer = []
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
        path = self.output_dir / f"{self.prefix}_part_{self.file_index:05d}.parquet"
        pq.write_table(table, path, compression="snappy")
        self.buffer.clear()
        self.file_index += 1

    def close(self) -> None:
        self.flush()


def make_rng(offset: int = 0) -> random.Random:
    return random.Random(SEED + offset)


def random_timestamp(rng: random.Random, years_back: int = 2) -> str:
    end = datetime.utcnow()
    start = end - timedelta(days=365 * years_back)
    delta_seconds = int((end - start).total_seconds())
    value = start + timedelta(seconds=rng.randint(0, delta_seconds))
    return value.strftime("%Y-%m-%d %H:%M:%S")


def random_date(rng: random.Random, years_back: int = 2) -> str:
    end = date.today()
    start = end - timedelta(days=365 * years_back)
    delta_days = (end - start).days
    value = start + timedelta(days=rng.randint(0, delta_days))
    return value.isoformat()


def random_person_name(rng: random.Random) -> tuple[str, str]:
    return rng.choice(FIRST_NAMES), rng.choice(LAST_NAMES)


def random_city_state(rng: random.Random) -> tuple[str, str]:
    return rng.choice(CITIES)


def random_company(rng: random.Random, prefix: str) -> str:
    return f"{prefix} {rng.choice(LAST_NAMES)} {rng.choice(['Inc', 'LLC', 'Corp', 'Group'])}"


def zip_directory(source_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        for _ in range(5):
            try:
                zip_path.unlink()
                break
            except PermissionError:
                time.sleep(0.2)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        for file_path in sorted(source_dir.rglob("*")):
            if file_path.is_file():
                handle.write(file_path, arcname=file_path.relative_to(source_dir.parent))


def zip_file(source_file: Path, zip_path: Path) -> None:
    if zip_path.exists():
        for _ in range(5):
            try:
                zip_path.unlink()
                break
            except PermissionError:
                time.sleep(0.2)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as handle:
        handle.write(source_file, arcname=source_file.name)


def write_parquet_zip(
    output_dir: Path,
    zip_name: str,
    folder_name: str,
    prefix: str,
    rows_per_file: int,
    row_count: int,
    row_builder,
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"{prefix}_") as temp_name:
        temp_dir = Path(temp_name)
        parquet_dir = temp_dir / folder_name
        writer = ChunkedParquetWriter(parquet_dir, prefix, rows_per_file)
        for index in range(1, row_count + 1):
            writer.write_row(row_builder(index))
        writer.close()
        zip_directory(parquet_dir, output_dir / zip_name)


def write_csv_zip(
    output_dir: Path,
    zip_name: str,
    file_name: str,
    columns: list[str],
    row_count: int,
    row_builder,
) -> None:
    with tempfile.TemporaryDirectory(prefix=f"{file_name}_") as temp_name:
        temp_dir = Path(temp_name)
        csv_path = temp_dir / file_name
        with csv_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(columns)
            for index in range(1, row_count + 1):
                writer.writerow(row_builder(index))
        zip_file(csv_path, output_dir / zip_name)
