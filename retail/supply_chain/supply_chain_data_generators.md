# 🧪 Supply Chain Data Generators

[🏠 Back to Home](../../readme.md)
[🚚 Back to Supply Chain Platform](supply_chain_full.md)

## 📌 Python Generator (100,000 Shipment Rows)
```python
from faker import Faker
import csv
import random

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)
ROWS = 100_000

def gen_dim_supplier(rows=5000, filename="dim_supplier.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["supplier_id","supplier_code","supplier_name","country_code","supplier_tier","is_active"])
        for i in range(1, rows + 1):
            w.writerow([i, f"SUP-{i:06d}", fake.company(), "USA", random.choice(["gold","silver","bronze"]), True])

def gen_dim_carrier(rows=200, filename="dim_carrier.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["carrier_id","carrier_code","carrier_name","service_level"])
        for i in range(1, rows + 1):
            w.writerow([i, f"CAR-{i:04d}", fake.company(), random.choice(["standard","expedited","overnight"])])

def gen_purchase_order(rows=ROWS, supplier_count=5000, warehouse_count=500, filename="purchase_order.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["po_id","po_number","supplier_id","warehouse_id","po_status","order_date","expected_date"])
        for i in range(1, rows + 1):
            order_date = fake.date_between(start_date="-2y", end_date="today")
            expected = fake.date_between(start_date=order_date, end_date="+30d")
            w.writerow([i, f"PO-{i:08d}", random.randint(1, supplier_count), random.randint(1, warehouse_count), random.choice(["created","approved","shipped","received","closed"]), order_date, expected])

def gen_shipment(rows=ROWS, po_count=ROWS, carrier_count=200, filename="shipment.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["shipment_id","shipment_number","po_id","carrier_id","shipment_status","shipped_ts","eta_ts","delivered_ts"])
        for i in range(1, rows + 1):
            shipped = fake.date_time_between(start_date="-2y", end_date="now")
            w.writerow([i, f"SHP-{i:08d}", random.randint(1, po_count), random.randint(1, carrier_count), random.choice(["created","in_transit","delivered","delayed"]), shipped, fake.date_time_between(start_date=shipped, end_date="+10d"), fake.date_time_between(start_date=shipped, end_date="+15d")])

if __name__ == "__main__":
    gen_dim_supplier()
    gen_dim_carrier()
    gen_purchase_order()
    gen_shipment()
    print("Generated supply chain CSV files.")
```
