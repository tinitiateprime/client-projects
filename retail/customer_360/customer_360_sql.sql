-- Customer 360 warehouse DDL

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
    interaction_type      VARCHAR(50) NOT NULL,
    channel               VARCHAR(30) NOT NULL,
    campaign_id           VARCHAR(50),
    interaction_ts        TIMESTAMP NOT NULL
);
