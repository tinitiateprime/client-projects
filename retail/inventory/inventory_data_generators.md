# 🧪 Inventory Data Generators

[🏠 Back to Home](../../readme.md)
[📦 Back to Inventory Platform](inventory_full.md)

## 📌 Python Generator (100,000 Records)
```python
from faker import Faker
import csv
import random

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)
ROWS = 100_000

def gen_dim_product(rows=ROWS, filename="dim_product.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["product_id","sku","product_name","category","brand","unit_cost","unit_price","is_active"])
        for i in range(1, rows + 1):
            cost = round(random.uniform(3, 200), 2)
            price = round(cost * random.uniform(1.1, 2.8), 2)
            w.writerow([i, f"SKU-{i:08d}", fake.word().upper(), fake.word(), fake.company(), cost, price, True])

def gen_dim_store(rows=1000, filename="dim_store.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["store_id","store_code","store_name","city","state_code","country_code","is_active"])
        for i in range(1, rows + 1):
            w.writerow([i, f"STR-{i:05d}", f"Store {i}", fake.city(), fake.state_abbr(), "USA", True])

def gen_dim_warehouse(rows=200, filename="dim_warehouse.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["warehouse_id","warehouse_code","warehouse_name","city","state_code","country_code","is_active"])
        for i in range(1, rows + 1):
            w.writerow([i, f"WH-{i:04d}", f"Warehouse {i}", fake.city(), fake.state_abbr(), "USA", True])

def gen_store_inventory(rows=ROWS, store_count=1000, product_count=ROWS, filename="store_inventory.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["store_inventory_id","store_id","product_id","on_hand_qty","reserved_qty","safety_stock_qty","reorder_point_qty"])
        for i in range(1, rows + 1):
            on_hand = random.randint(0, 500)
            reserved = random.randint(0, min(40, on_hand))
            w.writerow([i, random.randint(1, store_count), random.randint(1, product_count), on_hand, reserved, random.randint(10, 80), random.randint(20, 120)])

def gen_warehouse_inventory(rows=ROWS, warehouse_count=200, product_count=ROWS, filename="warehouse_inventory.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["warehouse_inventory_id","warehouse_id","product_id","on_hand_qty","allocated_qty","in_transit_in_qty","in_transit_out_qty","safety_stock_qty","reorder_point_qty"])
        for i in range(1, rows + 1):
            on_hand = random.randint(0, 5000)
            allocated = random.randint(0, min(500, on_hand))
            w.writerow([i, random.randint(1, warehouse_count), random.randint(1, product_count), on_hand, allocated, random.randint(0, 300), random.randint(0, 300), random.randint(50, 300), random.randint(100, 500)])

def gen_inventory_movement(rows=ROWS, product_count=ROWS, store_count=1000, warehouse_count=200, filename="inventory_movement.csv"):
    movement_types = ["sale","return","transfer_in","transfer_out","receive_po","adjustment"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["movement_id","product_id","movement_type","source_store_id","source_warehouse_id","target_store_id","target_warehouse_id","quantity","reference_type","reference_id","movement_ts"])
        for i in range(1, rows + 1):
            mtype = random.choice(movement_types)
            w.writerow([i, random.randint(1, product_count), mtype, random.randint(1, store_count), random.randint(1, warehouse_count), random.randint(1, store_count), random.randint(1, warehouse_count), random.randint(1, 200), "ops", f"REF-{i:08d}", fake.date_time_between(start_date="-2y", end_date="now")])

if __name__ == "__main__":
    gen_dim_product()
    gen_dim_store()
    gen_dim_warehouse()
    gen_store_inventory()
    gen_warehouse_inventory()
    gen_inventory_movement()
    print("Generated inventory CSV files.")
```
