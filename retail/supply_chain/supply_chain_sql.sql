-- Supply chain warehouse DDL

CREATE TABLE dim_supplier (
    supplier_id          BIGSERIAL PRIMARY KEY,
    supplier_code        VARCHAR(40) NOT NULL UNIQUE,
    supplier_name        VARCHAR(150) NOT NULL,
    country_code         VARCHAR(3) NOT NULL DEFAULT 'USA',
    supplier_tier        VARCHAR(30),
    is_active            BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE dim_carrier (
    carrier_id           BIGSERIAL PRIMARY KEY,
    carrier_code         VARCHAR(40) NOT NULL UNIQUE,
    carrier_name         VARCHAR(150) NOT NULL,
    service_level        VARCHAR(50)
);

CREATE TABLE dim_warehouse (
    warehouse_id         BIGSERIAL PRIMARY KEY,
    warehouse_code       VARCHAR(30) NOT NULL UNIQUE,
    warehouse_name       VARCHAR(150) NOT NULL,
    city                 VARCHAR(100),
    state_code           VARCHAR(10),
    country_code         VARCHAR(3) NOT NULL DEFAULT 'USA'
);

CREATE TABLE purchase_order (
    po_id                BIGSERIAL PRIMARY KEY,
    po_number            VARCHAR(60) NOT NULL UNIQUE,
    supplier_id          BIGINT NOT NULL REFERENCES dim_supplier(supplier_id),
    warehouse_id         BIGINT NOT NULL REFERENCES dim_warehouse(warehouse_id),
    po_status            VARCHAR(30) NOT NULL,
    order_date           DATE NOT NULL,
    expected_date        DATE
);

CREATE TABLE purchase_order_line (
    po_line_id           BIGSERIAL PRIMARY KEY,
    po_id                BIGINT NOT NULL REFERENCES purchase_order(po_id),
    sku                  VARCHAR(50) NOT NULL,
    ordered_qty          INTEGER NOT NULL,
    unit_cost            DECIMAL(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE shipment (
    shipment_id          BIGSERIAL PRIMARY KEY,
    shipment_number      VARCHAR(60) NOT NULL UNIQUE,
    po_id                BIGINT NOT NULL REFERENCES purchase_order(po_id),
    carrier_id           BIGINT REFERENCES dim_carrier(carrier_id),
    shipment_status      VARCHAR(30) NOT NULL,
    shipped_ts           TIMESTAMP,
    eta_ts               TIMESTAMP,
    delivered_ts         TIMESTAMP
);

CREATE TABLE shipment_line (
    shipment_line_id     BIGSERIAL PRIMARY KEY,
    shipment_id          BIGINT NOT NULL REFERENCES shipment(shipment_id),
    sku                  VARCHAR(50) NOT NULL,
    shipped_qty          INTEGER NOT NULL,
    damaged_qty          INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE receiving_event (
    receiving_event_id   BIGSERIAL PRIMARY KEY,
    shipment_id          BIGINT NOT NULL REFERENCES shipment(shipment_id),
    warehouse_id         BIGINT NOT NULL REFERENCES dim_warehouse(warehouse_id),
    sku                  VARCHAR(50) NOT NULL,
    received_qty         INTEGER NOT NULL,
    received_ts          TIMESTAMP NOT NULL,
    is_partial           BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE fact_supply_chain_kpi (
    kpi_id               BIGSERIAL PRIMARY KEY,
    warehouse_id         BIGINT REFERENCES dim_warehouse(warehouse_id),
    supplier_id          BIGINT REFERENCES dim_supplier(supplier_id),
    kpi_date             DATE NOT NULL,
    on_time_delivery_pct DECIMAL(5,2),
    fill_rate_pct        DECIMAL(5,2),
    avg_lead_time_days   DECIMAL(8,2),
    damaged_rate_pct     DECIMAL(5,2)
);
