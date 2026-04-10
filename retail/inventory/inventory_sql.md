# 🧱 Inventory SQL Pack

[🏠 Back to Home](../../readme.md)
[📦 Back to Inventory Platform](inventory_full.md)

## 📌 Core DDL
```sql
CREATE TABLE dim_product (
    product_id           BIGSERIAL PRIMARY KEY,
    sku                  VARCHAR(50) NOT NULL UNIQUE,
    product_name         VARCHAR(200) NOT NULL,
    category             VARCHAR(100),
    brand                VARCHAR(100),
    unit_cost            DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    unit_price           DECIMAL(12,2) NOT NULL DEFAULT 0.00,
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_store (
    store_id             BIGSERIAL PRIMARY KEY,
    store_code           VARCHAR(30) NOT NULL UNIQUE,
    store_name           VARCHAR(150) NOT NULL,
    city                 VARCHAR(100),
    state_code           VARCHAR(10),
    country_code         VARCHAR(3) NOT NULL DEFAULT 'USA',
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE dim_warehouse (
    warehouse_id         BIGSERIAL PRIMARY KEY,
    warehouse_code       VARCHAR(30) NOT NULL UNIQUE,
    warehouse_name       VARCHAR(150) NOT NULL,
    city                 VARCHAR(100),
    state_code           VARCHAR(10),
    country_code         VARCHAR(3) NOT NULL DEFAULT 'USA',
    is_active            BOOLEAN NOT NULL DEFAULT TRUE,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE store_inventory (
    store_inventory_id   BIGSERIAL PRIMARY KEY,
    store_id             BIGINT NOT NULL REFERENCES dim_store(store_id),
    product_id           BIGINT NOT NULL REFERENCES dim_product(product_id),
    on_hand_qty          INTEGER NOT NULL DEFAULT 0,
    reserved_qty         INTEGER NOT NULL DEFAULT 0,
    safety_stock_qty     INTEGER NOT NULL DEFAULT 0,
    reorder_point_qty    INTEGER NOT NULL DEFAULT 0,
    updated_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (store_id, product_id)
);

CREATE TABLE warehouse_inventory (
    warehouse_inventory_id BIGSERIAL PRIMARY KEY,
    warehouse_id         BIGINT NOT NULL REFERENCES dim_warehouse(warehouse_id),
    product_id           BIGINT NOT NULL REFERENCES dim_product(product_id),
    on_hand_qty          INTEGER NOT NULL DEFAULT 0,
    allocated_qty        INTEGER NOT NULL DEFAULT 0,
    in_transit_in_qty    INTEGER NOT NULL DEFAULT 0,
    in_transit_out_qty   INTEGER NOT NULL DEFAULT 0,
    safety_stock_qty     INTEGER NOT NULL DEFAULT 0,
    reorder_point_qty    INTEGER NOT NULL DEFAULT 0,
    updated_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (warehouse_id, product_id)
);

CREATE TABLE inventory_movement (
    movement_id          BIGSERIAL PRIMARY KEY,
    product_id           BIGINT NOT NULL REFERENCES dim_product(product_id),
    movement_type        VARCHAR(30) NOT NULL,
    source_store_id      BIGINT REFERENCES dim_store(store_id),
    source_warehouse_id  BIGINT REFERENCES dim_warehouse(warehouse_id),
    target_store_id      BIGINT REFERENCES dim_store(store_id),
    target_warehouse_id  BIGINT REFERENCES dim_warehouse(warehouse_id),
    quantity             INTEGER NOT NULL,
    reference_type       VARCHAR(30),
    reference_id         VARCHAR(80),
    movement_ts          TIMESTAMP NOT NULL,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_order (
    po_id                BIGSERIAL PRIMARY KEY,
    po_number            VARCHAR(50) NOT NULL UNIQUE,
    supplier_name        VARCHAR(150) NOT NULL,
    warehouse_id         BIGINT NOT NULL REFERENCES dim_warehouse(warehouse_id),
    po_status            VARCHAR(30) NOT NULL,
    order_date           DATE NOT NULL,
    expected_date        DATE,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE purchase_order_line (
    po_line_id           BIGSERIAL PRIMARY KEY,
    po_id                BIGINT NOT NULL REFERENCES purchase_order(po_id),
    product_id           BIGINT NOT NULL REFERENCES dim_product(product_id),
    ordered_qty          INTEGER NOT NULL,
    received_qty         INTEGER NOT NULL DEFAULT 0,
    unit_cost            DECIMAL(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE stock_transfer (
    transfer_id          BIGSERIAL PRIMARY KEY,
    transfer_number      VARCHAR(50) NOT NULL UNIQUE,
    source_type          VARCHAR(20) NOT NULL,
    source_id            BIGINT NOT NULL,
    target_type          VARCHAR(20) NOT NULL,
    target_id            BIGINT NOT NULL,
    transfer_status      VARCHAR(30) NOT NULL,
    requested_date       DATE NOT NULL,
    shipped_date         DATE,
    received_date        DATE,
    created_at           TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE stock_transfer_line (
    transfer_line_id     BIGSERIAL PRIMARY KEY,
    transfer_id          BIGINT NOT NULL REFERENCES stock_transfer(transfer_id),
    product_id           BIGINT NOT NULL REFERENCES dim_product(product_id),
    requested_qty        INTEGER NOT NULL,
    shipped_qty          INTEGER NOT NULL DEFAULT 0,
    received_qty         INTEGER NOT NULL DEFAULT 0
);
```

## 📊 Reporting SQL
```sql
SELECT
    s.store_code,
    p.sku,
    p.product_name,
    si.on_hand_qty - si.reserved_qty AS available_qty
FROM store_inventory si
JOIN dim_store s ON s.store_id = si.store_id
JOIN dim_product p ON p.product_id = si.product_id;

SELECT
    w.warehouse_code,
    p.sku,
    p.product_name,
    wi.on_hand_qty - wi.allocated_qty AS net_available_qty
FROM warehouse_inventory wi
JOIN dim_warehouse w ON w.warehouse_id = wi.warehouse_id
JOIN dim_product p ON p.product_id = wi.product_id;
```
