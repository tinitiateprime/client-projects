-- Sales warehouse DDL

CREATE TABLE dim_date (
    date_key             INTEGER PRIMARY KEY,
    full_date            DATE NOT NULL,
    day_of_week          INTEGER,
    month_num            INTEGER,
    quarter_num          INTEGER,
    year_num             INTEGER
);

CREATE TABLE dim_product (
    product_id           BIGSERIAL PRIMARY KEY,
    sku                  VARCHAR(50) NOT NULL UNIQUE,
    product_name         VARCHAR(200) NOT NULL,
    category             VARCHAR(100),
    brand                VARCHAR(100)
);

CREATE TABLE dim_store (
    store_id             BIGSERIAL PRIMARY KEY,
    store_code           VARCHAR(30) NOT NULL UNIQUE,
    store_name           VARCHAR(150) NOT NULL,
    city                 VARCHAR(100),
    state_code           VARCHAR(10),
    country_code         VARCHAR(3) NOT NULL DEFAULT 'USA'
);

CREATE TABLE dim_channel (
    channel_id           BIGSERIAL PRIMARY KEY,
    channel_name         VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE fact_sales (
    sales_id             BIGSERIAL PRIMARY KEY,
    order_id             VARCHAR(60) NOT NULL,
    order_line_id        VARCHAR(80) NOT NULL,
    date_key             INTEGER NOT NULL REFERENCES dim_date(date_key),
    product_id           BIGINT NOT NULL REFERENCES dim_product(product_id),
    store_id             BIGINT REFERENCES dim_store(store_id),
    channel_id           BIGINT NOT NULL REFERENCES dim_channel(channel_id),
    quantity             INTEGER NOT NULL,
    gross_amount         DECIMAL(12,2) NOT NULL,
    discount_amount      DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    tax_amount           DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    net_amount           DECIMAL(12,2) NOT NULL,
    cost_amount          DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    margin_amount        DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    order_ts             TIMESTAMP NOT NULL,
    UNIQUE (order_line_id)
);

CREATE TABLE fact_returns (
    return_id            BIGSERIAL PRIMARY KEY,
    sales_id             BIGINT NOT NULL REFERENCES fact_sales(sales_id),
    return_reason        VARCHAR(100),
    return_qty           INTEGER NOT NULL,
    return_amount        DECIMAL(12,2) NOT NULL,
    return_ts            TIMESTAMP NOT NULL
);

CREATE TABLE fact_promotion_redemption (
    promo_redemption_id  BIGSERIAL PRIMARY KEY,
    sales_id             BIGINT NOT NULL REFERENCES fact_sales(sales_id),
    promo_code           VARCHAR(60) NOT NULL,
    promo_type           VARCHAR(30),
    discount_amount      DECIMAL(12,2) NOT NULL,
    redemption_ts        TIMESTAMP NOT NULL
);

CREATE TABLE fact_sales_target (
    target_id            BIGSERIAL PRIMARY KEY,
    date_key             INTEGER NOT NULL REFERENCES dim_date(date_key),
    store_id             BIGINT REFERENCES dim_store(store_id),
    channel_id           BIGINT NOT NULL REFERENCES dim_channel(channel_id),
    target_net_sales     DECIMAL(14,2) NOT NULL,
    target_units         INTEGER NOT NULL
);
