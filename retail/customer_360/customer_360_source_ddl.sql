-- Customer 360 source landing DDL
-- Design: all inbound records land in one source table.
-- Data can arrive from POS sales feeds, CRM customer feeds, or CSV files.
-- ETL/ELT logic then separates the data into the target warehouse tables.

CREATE SCHEMA IF NOT EXISTS src;

CREATE TABLE src.customer_360_landing (
    landing_id            BIGSERIAL PRIMARY KEY,
    batch_id              VARCHAR(100) NOT NULL,
    record_source         VARCHAR(20) NOT NULL,   -- POS, CRM, CSV
    record_type           VARCHAR(30) NOT NULL,   -- CUSTOMER, CONTACT, ADDRESS, ORDER, INTERACTION
    source_file_name      VARCHAR(255),
    source_row_number     BIGINT,
    source_record_id      VARCHAR(100),

    customer_id           VARCHAR(100),
    source_customer_id    VARCHAR(100),
    first_name            VARCHAR(100),
    middle_name           VARCHAR(100),
    last_name             VARCHAR(100),
    dob                   DATE,
    gender                VARCHAR(20),
    ssn                   VARCHAR(50),

    email_address         VARCHAR(255),
    phone_number          VARCHAR(25),
    phone_type            VARCHAR(20),
    is_verified           BOOLEAN,
    opt_in_marketing      BOOLEAN,

    address_type          VARCHAR(20),
    address_line_1        VARCHAR(200),
    address_line_2        VARCHAR(200),
    city                  VARCHAR(100),
    state_code            VARCHAR(10),
    postal_code           VARCHAR(20),
    country_code          VARCHAR(3),

    order_id              VARCHAR(100),
    channel               VARCHAR(30),
    payment_type          VARCHAR(30),
    status                VARCHAR(20),
    gross_amount          DECIMAL(12,2),
    discount_amount       DECIMAL(12,2),
    net_amount            DECIMAL(12,2),

    interaction_type      VARCHAR(50),
    campaign_id           VARCHAR(50),
    event_ts              TIMESTAMP,

    ingest_ts             TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    raw_payload           TEXT
);

-- Example target separation logic:
-- CUSTOMER rows populate dim_customer
-- ADDRESS rows populate dim_customer_address
-- CONTACT rows populate dim_customer_email and dim_customer_phone
-- ORDER rows populate fact_order
-- INTERACTION rows populate fact_customer_interaction
