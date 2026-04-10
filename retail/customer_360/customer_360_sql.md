# 🧱 Customer 360 SQL Pack

[🏠 Back to Home](../../readme.md)
[🧩 Back to Personalization Platform](customer_platform.md)

## 📌 Overview
This document centralizes all SQL used by the Customer 360 project:
- Core Customer 360 DDL
- Duplicate detection SQL
- dbt model SQL examples

## 🧱 Core DDL (Customer Key: `customer_id`)
```sql
CREATE TABLE dim_customer (
  customer_id BIGSERIAL PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  middle_name VARCHAR(100),
  last_name VARCHAR(100) NOT NULL,
  dob DATE NOT NULL,
  gender VARCHAR(20) NOT NULL,
  ssn VARCHAR(11) NOT NULL UNIQUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer_address (
  address_id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES dim_customer(customer_id),
  address_type VARCHAR(20) NOT NULL,
  address_line_1 VARCHAR(200) NOT NULL,
  address_line_2 VARCHAR(200),
  city VARCHAR(100) NOT NULL,
  state_code VARCHAR(10) NOT NULL,
  postal_code VARCHAR(20) NOT NULL,
  country_code VARCHAR(3) NOT NULL DEFAULT 'USA',
  is_primary BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer_phone (
  phone_id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES dim_customer(customer_id),
  phone_type VARCHAR(20) NOT NULL,
  country_code VARCHAR(5) NOT NULL DEFAULT '+1',
  phone_number VARCHAR(25) NOT NULL,
  is_primary BOOLEAN NOT NULL DEFAULT TRUE,
  is_verified BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer_email (
  email_id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES dim_customer(customer_id),
  email_address VARCHAR(255) NOT NULL UNIQUE,
  is_primary BOOLEAN NOT NULL DEFAULT TRUE,
  is_verified BOOLEAN NOT NULL DEFAULT FALSE,
  opt_in_marketing BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_transaction (
  transaction_id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES dim_customer(customer_id),
  order_id VARCHAR(50) NOT NULL UNIQUE,
  channel VARCHAR(30) NOT NULL,
  payment_type VARCHAR(30) NOT NULL,
  status VARCHAR(20) NOT NULL,
  gross_amount DECIMAL(12,2) NOT NULL,
  discount_amount DECIMAL(12,2) NOT NULL,
  net_amount DECIMAL(12,2) NOT NULL,
  transaction_ts TIMESTAMP NOT NULL
);

CREATE TABLE fact_customer_interaction (
  interaction_id BIGSERIAL PRIMARY KEY,
  customer_id BIGINT NOT NULL REFERENCES dim_customer(customer_id),
  interaction_type VARCHAR(50) NOT NULL,
  channel VARCHAR(30) NOT NULL,
  campaign_id VARCHAR(50),
  interaction_ts TIMESTAMP NOT NULL
);
```

## 🧱 Alternate DDL (Customer Key: `customer_sk`)
```sql
CREATE TABLE dim_customer (
    customer_sk           BIGSERIAL PRIMARY KEY,
    first_name            VARCHAR(100),
    middle_name           VARCHAR(100),
    last_name             VARCHAR(100),
    dob                   DATE NOT NULL,
    gender                VARCHAR(20) NOT NULL,
    ssn                   VARCHAR(11) UNIQUE NOT NULL,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer_address (
    address_sk            BIGSERIAL PRIMARY KEY,
    customer_sk           BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    address_type          VARCHAR(20) NOT NULL,
    address_line_1        VARCHAR(200) NOT NULL,
    address_line_2        VARCHAR(200),
    city                  VARCHAR(100) NOT NULL,
    state_code            VARCHAR(10) NOT NULL,
    postal_code           VARCHAR(20) NOT NULL,
    country_code          VARCHAR(3) NOT NULL DEFAULT 'USA',
    is_primary            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer_phone (
    phone_sk              BIGSERIAL PRIMARY KEY,
    customer_sk           BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    phone_type            VARCHAR(20) NOT NULL,
    country_code          VARCHAR(5) NOT NULL DEFAULT '+1',
    phone_number          VARCHAR(25) NOT NULL,
    is_primary            BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified           BOOLEAN NOT NULL DEFAULT FALSE,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_customer_email (
    email_sk              BIGSERIAL PRIMARY KEY,
    customer_sk           BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    email_address         VARCHAR(255) NOT NULL UNIQUE,
    is_primary            BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified           BOOLEAN NOT NULL DEFAULT FALSE,
    opt_in_marketing      BOOLEAN NOT NULL DEFAULT TRUE,
    created_at            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fact_order (
    order_sk              BIGSERIAL PRIMARY KEY,
    customer_sk           BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    order_id              VARCHAR(100) NOT NULL,
    channel               VARCHAR(30) NOT NULL,
    payment_type          VARCHAR(30) NOT NULL,
    status                VARCHAR(20) NOT NULL,
    gross_amount          DECIMAL(12,2) NOT NULL,
    discount_amount       DECIMAL(12,2) NOT NULL,
    net_amount            DECIMAL(12,2) NOT NULL,
    order_ts              TIMESTAMP NOT NULL
);

CREATE TABLE fact_customer_interaction (
    interaction_sk        BIGSERIAL PRIMARY KEY,
    customer_sk           BIGINT NOT NULL REFERENCES dim_customer(customer_sk),
    interaction_type      VARCHAR(100) NOT NULL,
    channel               VARCHAR(50) NOT NULL,
    campaign_id           VARCHAR(100),
    interaction_ts        TIMESTAMP NOT NULL
);
```

## 🧱 Duplicate Detection SQL
```sql
SELECT
  lower(trim(email_address)) AS normalized_email,
  COUNT(*) AS cnt
FROM dim_customer_email
GROUP BY lower(trim(email_address))
HAVING COUNT(*) > 1
ORDER BY cnt DESC;
```

```sql
SELECT
    lower(trim(email_address)) AS normalized_email,
    COUNT(*) AS duplicate_count
FROM dim_customer_email
GROUP BY lower(trim(email_address))
HAVING COUNT(*) > 1
ORDER BY duplicate_count DESC;
```

## 🧱 dbt SQL Models
```sql
-- models/staging/stg_orders.sql
select
    order_id,
    source_customer_id,
    channel,
    cast(gross_amount as numeric(12,2)) as gross_amount,
    cast(discount_amount as numeric(12,2)) as discount_amount,
    cast(order_ts as timestamp) as order_ts
from {{ source('raw', 'orders') }}
```

```sql
-- models/marts/customer_360/fct_customer_value.sql
select
    c.customer_sk,
    count(o.order_id) as order_count,
    sum(o.net_amount) as lifetime_value,
    max(o.order_ts) as last_order_ts
from {{ ref('dim_customer') }} c
left join {{ ref('fact_order') }} o
    on c.customer_sk = o.customer_sk
group by 1
```

