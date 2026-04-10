# 🧪 Sales Data Generators

[🏠 Back to Home](../../readme.md)
[📈 Back to Sales Platform](sales_full.md)

## 📌 Python Generator (100,000 Sales Rows)
```python
from faker import Faker
import csv
import random
from datetime import datetime

fake = Faker("en_US")
Faker.seed(42)
random.seed(42)
ROWS = 100_000

def gen_dim_product(rows=ROWS, filename="dim_product.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["product_id","sku","product_name","category","brand"])
        for i in range(1, rows + 1):
            w.writerow([i, f"SKU-{i:08d}", fake.word().upper(), fake.word(), fake.company()])

def gen_dim_store(rows=1000, filename="dim_store.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["store_id","store_code","store_name","city","state_code","country_code"])
        for i in range(1, rows + 1):
            w.writerow([i, f"STR-{i:05d}", f"Store {i}", fake.city(), fake.state_abbr(), "USA"])

def gen_dim_channel(filename="dim_channel.csv"):
    channels = ["store", "web", "app", "marketplace"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["channel_id","channel_name"])
        for i, c in enumerate(channels, 1):
            w.writerow([i, c])

def gen_fact_sales(rows=ROWS, product_count=ROWS, store_count=1000, filename="fact_sales.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sales_id","order_id","order_line_id","date_key","product_id","store_id","channel_id","quantity","gross_amount","discount_amount","tax_amount","net_amount","cost_amount","margin_amount","order_ts"])
        for i in range(1, rows + 1):
            qty = random.randint(1, 8)
            gross = round(random.uniform(10, 1200), 2)
            disc = round(random.uniform(0, gross * 0.30), 2)
            tax = round((gross - disc) * 0.08, 2)
            net = round(gross - disc + tax, 2)
            cost = round((gross - disc) * random.uniform(0.45, 0.85), 2)
            margin = round(net - cost, 2)
            dt = fake.date_time_between(start_date="-2y", end_date="now")
            date_key = int(dt.strftime("%Y%m%d"))
            w.writerow([i, f"ORD-{i:08d}", f"ORDL-{i:09d}", date_key, random.randint(1, product_count), random.randint(1, store_count), random.randint(1, 4), qty, gross, disc, tax, net, cost, margin, dt])

def gen_fact_returns(rows=20_000, sales_count=ROWS, filename="fact_returns.csv"):
    reasons = ["damaged", "wrong_item", "size_issue", "late_delivery", "customer_remorse"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["return_id","sales_id","return_reason","return_qty","return_amount","return_ts"])
        for i in range(1, rows + 1):
            w.writerow([i, random.randint(1, sales_count), random.choice(reasons), random.randint(1, 3), round(random.uniform(5, 300), 2), fake.date_time_between(start_date="-2y", end_date="now")])

if __name__ == "__main__":
    gen_dim_product()
    gen_dim_store()
    gen_dim_channel()
    gen_fact_sales()
    gen_fact_returns()
    print("Generated sales CSV files.")
```
