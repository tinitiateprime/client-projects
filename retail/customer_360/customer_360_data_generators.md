# 🧪 Customer 360 Data Generators

[🏠 Back to Home](../../readme.md)
[🧩 Back to Personalization Platform](customer_platform.md)

## 📌 Python Generator (100,000 Records Per Table)
```python
from faker import Faker
import csv
import random
from datetime import datetime, timedelta

fake = Faker("en_US")
random.seed(42)
Faker.seed(42)
ROWS_PER_TABLE = 100_000

def generate_customers(filename="dim_customer.csv", rows=ROWS_PER_TABLE):
    genders = ["male", "female", "non_binary", "unknown"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "customer_sk","first_name","middle_name","last_name",
            "dob","gender","ssn","created_at","updated_at"
        ])
        for i in range(1, rows + 1):
            first = fake.first_name()
            middle = fake.first_name() if random.random() < 0.55 else ""
            last = fake.last_name()
            dob = fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat()
            gender = random.choice(genders)
            ssn = fake.ssn()
            ts = fake.date_time_between(start_date="-3y", end_date="now")
            w.writerow([
                i,
                first,
                middle,
                last,
                dob,
                gender,
                ssn,
                ts,
                ts
            ])

def generate_customer_addresses(filename="dim_customer_address.csv", rows=ROWS_PER_TABLE):
    address_types = ["home", "billing", "shipping"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "address_sk","customer_sk","address_type","address_line_1","address_line_2",
            "city","state_code","postal_code","country_code","is_primary","created_at"
        ])
        for i in range(1, rows + 1):
            w.writerow([
                i,
                i,
                random.choice(address_types),
                fake.street_address(),
                fake.secondary_address() if random.random() < 0.35 else "",
                fake.city(),
                fake.state_abbr(),
                fake.postcode(),
                "USA",
                True,
                fake.date_time_between(start_date="-3y", end_date="now")
            ])

def generate_customer_phones(filename="dim_customer_phone.csv", rows=ROWS_PER_TABLE):
    phone_types = ["mobile", "home", "work"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "phone_sk","customer_sk","phone_type","country_code","phone_number",
            "is_primary","is_verified","created_at"
        ])
        for i in range(1, rows + 1):
            w.writerow([
                i,
                i,
                random.choice(phone_types),
                "+1",
                fake.numerify("##########"),
                True,
                random.choice([True, False]),
                fake.date_time_between(start_date="-3y", end_date="now")
            ])

def generate_customer_emails(filename="dim_customer_email.csv", rows=ROWS_PER_TABLE):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "email_sk","customer_sk","email_address","is_primary",
            "is_verified","opt_in_marketing","created_at"
        ])
        for i in range(1, rows + 1):
            w.writerow([
                i,
                i,
                f"user{i}@example.com",
                True,
                random.choice([True, True, False]),
                random.choice([True, True, False]),
                fake.date_time_between(start_date="-3y", end_date="now")
            ])

def generate_orders(filename="fact_order.csv", rows=ROWS_PER_TABLE, customer_count=ROWS_PER_TABLE):
    channels = ["store", "web", "app"]
    payment_types = ["card", "cash", "wallet"]
    statuses = ["completed", "refunded", "cancelled"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "order_sk","customer_sk","order_id","channel",
            "payment_type","status","gross_amount","discount_amount","net_amount","order_ts"
        ])
        for i in range(1, rows + 1):
            gross = round(random.uniform(10, 1500), 2)
            disc = round(random.uniform(0, gross * 0.25), 2)
            w.writerow([
                i,
                random.randint(1, customer_count),
                f"ORD{i:07d}",
                random.choice(channels),
                random.choice(payment_types),
                random.choice(statuses),
                gross,
                disc,
                round(gross - disc, 2),
                fake.date_time_between(start_date="-2y", end_date="now")
            ])

def generate_interactions(filename="fact_customer_interaction.csv", rows=ROWS_PER_TABLE, customer_count=ROWS_PER_TABLE):
    interaction_types = ["page_view", "click", "email_open", "sms_click", "call"]
    channels = ["web", "app", "email", "sms", "call_center"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "interaction_sk","customer_sk","interaction_type","channel","campaign_id","interaction_ts"
        ])
        for i in range(1, rows + 1):
            w.writerow([
                i,
                random.randint(1, customer_count),
                random.choice(interaction_types),
                random.choice(channels),
                f"CMP-{random.randint(1, 2500):05d}",
                fake.date_time_between(start_date="-2y", end_date="now")
            ])

if __name__ == "__main__":
    generate_customers()
    generate_customer_addresses()
    generate_customer_phones()
    generate_customer_emails()
    generate_orders()
    generate_interactions()
    print("Generated 100,000 records for each Customer 360 table.")
```

