-- Inventory source-side ingestion objects for SQL Server

IF OBJECT_ID('dbo.inventory_product_source', 'U') IS NOT NULL DROP TABLE dbo.inventory_product_source;
GO
IF OBJECT_ID('dbo.inventory_store_source', 'U') IS NOT NULL DROP TABLE dbo.inventory_store_source;
GO
IF OBJECT_ID('dbo.inventory_warehouse_source', 'U') IS NOT NULL DROP TABLE dbo.inventory_warehouse_source;
GO
IF OBJECT_ID('dbo.store_inventory_source', 'U') IS NOT NULL DROP TABLE dbo.store_inventory_source;
GO
IF OBJECT_ID('dbo.warehouse_inventory_source', 'U') IS NOT NULL DROP TABLE dbo.warehouse_inventory_source;
GO
IF OBJECT_ID('dbo.inventory_movement_source', 'U') IS NOT NULL DROP TABLE dbo.inventory_movement_source;
GO
IF OBJECT_ID('dbo.purchase_order_source', 'U') IS NOT NULL DROP TABLE dbo.purchase_order_source;
GO
IF OBJECT_ID('dbo.purchase_order_line_source', 'U') IS NOT NULL DROP TABLE dbo.purchase_order_line_source;
GO
IF OBJECT_ID('dbo.stock_transfer_source', 'U') IS NOT NULL DROP TABLE dbo.stock_transfer_source;
GO
IF OBJECT_ID('dbo.stock_transfer_line_source', 'U') IS NOT NULL DROP TABLE dbo.stock_transfer_line_source;
GO

CREATE TABLE dbo.inventory_product_source (
    product_id           BIGINT NOT NULL PRIMARY KEY,
    sku                  VARCHAR(50) NOT NULL,
    product_name         VARCHAR(200) NOT NULL,
    category             VARCHAR(100) NULL,
    brand                VARCHAR(100) NULL,
    unit_cost            DECIMAL(12,2) NOT NULL,
    unit_price           DECIMAL(12,2) NOT NULL,
    is_active            BIT NOT NULL,
    created_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.inventory_store_source (
    store_id             BIGINT NOT NULL PRIMARY KEY,
    store_code           VARCHAR(30) NOT NULL,
    store_name           VARCHAR(150) NOT NULL,
    city                 VARCHAR(100) NULL,
    state_code           VARCHAR(10) NULL,
    country_code         VARCHAR(3) NOT NULL,
    is_active            BIT NOT NULL,
    created_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.inventory_warehouse_source (
    warehouse_id         BIGINT NOT NULL PRIMARY KEY,
    warehouse_code       VARCHAR(30) NOT NULL,
    warehouse_name       VARCHAR(150) NOT NULL,
    city                 VARCHAR(100) NULL,
    state_code           VARCHAR(10) NULL,
    country_code         VARCHAR(3) NOT NULL,
    is_active            BIT NOT NULL,
    created_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.store_inventory_source (
    store_inventory_id   BIGINT NOT NULL PRIMARY KEY,
    store_id             BIGINT NOT NULL,
    product_id           BIGINT NOT NULL,
    on_hand_qty          INT NOT NULL,
    reserved_qty         INT NOT NULL,
    safety_stock_qty     INT NOT NULL,
    reorder_point_qty    INT NOT NULL,
    updated_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.warehouse_inventory_source (
    warehouse_inventory_id BIGINT NOT NULL PRIMARY KEY,
    warehouse_id         BIGINT NOT NULL,
    product_id           BIGINT NOT NULL,
    on_hand_qty          INT NOT NULL,
    allocated_qty        INT NOT NULL,
    in_transit_in_qty    INT NOT NULL,
    in_transit_out_qty   INT NOT NULL,
    safety_stock_qty     INT NOT NULL,
    reorder_point_qty    INT NOT NULL,
    updated_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.inventory_movement_source (
    movement_id          BIGINT NOT NULL PRIMARY KEY,
    product_id           BIGINT NOT NULL,
    movement_type        VARCHAR(30) NOT NULL,
    source_store_id      BIGINT NULL,
    source_warehouse_id  BIGINT NULL,
    target_store_id      BIGINT NULL,
    target_warehouse_id  BIGINT NULL,
    quantity             INT NOT NULL,
    reference_type       VARCHAR(30) NULL,
    reference_id         VARCHAR(80) NULL,
    movement_ts          DATETIME2 NOT NULL,
    created_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.purchase_order_source (
    po_id                BIGINT NOT NULL PRIMARY KEY,
    po_number            VARCHAR(50) NOT NULL,
    supplier_name        VARCHAR(150) NOT NULL,
    warehouse_id         BIGINT NOT NULL,
    po_status            VARCHAR(30) NOT NULL,
    order_date           DATE NOT NULL,
    expected_date        DATE NULL,
    created_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.purchase_order_line_source (
    po_line_id           BIGINT NOT NULL PRIMARY KEY,
    po_id                BIGINT NOT NULL,
    product_id           BIGINT NOT NULL,
    ordered_qty          INT NOT NULL,
    received_qty         INT NOT NULL,
    unit_cost            DECIMAL(12,2) NOT NULL
);
GO

CREATE TABLE dbo.stock_transfer_source (
    transfer_id          BIGINT NOT NULL PRIMARY KEY,
    transfer_number      VARCHAR(50) NOT NULL,
    source_type          VARCHAR(20) NOT NULL,
    source_id            BIGINT NOT NULL,
    target_type          VARCHAR(20) NOT NULL,
    target_id            BIGINT NOT NULL,
    transfer_status      VARCHAR(30) NOT NULL,
    requested_date       DATE NOT NULL,
    shipped_date         DATE NULL,
    received_date        DATE NULL,
    created_at           DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.stock_transfer_line_source (
    transfer_line_id     BIGINT NOT NULL PRIMARY KEY,
    transfer_id          BIGINT NOT NULL,
    product_id           BIGINT NOT NULL,
    requested_qty        INT NOT NULL,
    shipped_qty          INT NOT NULL,
    received_qty         INT NOT NULL
);
GO
