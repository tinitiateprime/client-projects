-- Supply chain source-side ingestion objects for SQL Server

IF OBJECT_ID('dbo.supplier_source', 'U') IS NOT NULL DROP TABLE dbo.supplier_source;
GO
IF OBJECT_ID('dbo.carrier_source', 'U') IS NOT NULL DROP TABLE dbo.carrier_source;
GO
IF OBJECT_ID('dbo.supply_chain_warehouse_source', 'U') IS NOT NULL DROP TABLE dbo.supply_chain_warehouse_source;
GO
IF OBJECT_ID('dbo.purchase_order_source', 'U') IS NOT NULL DROP TABLE dbo.purchase_order_source;
GO
IF OBJECT_ID('dbo.purchase_order_line_source', 'U') IS NOT NULL DROP TABLE dbo.purchase_order_line_source;
GO
IF OBJECT_ID('dbo.shipment_source', 'U') IS NOT NULL DROP TABLE dbo.shipment_source;
GO
IF OBJECT_ID('dbo.shipment_line_source', 'U') IS NOT NULL DROP TABLE dbo.shipment_line_source;
GO
IF OBJECT_ID('dbo.receiving_event_source', 'U') IS NOT NULL DROP TABLE dbo.receiving_event_source;
GO

CREATE TABLE dbo.supplier_source (
    supplier_id          BIGINT NOT NULL PRIMARY KEY,
    supplier_code        VARCHAR(40) NOT NULL,
    supplier_name        VARCHAR(150) NOT NULL,
    country_code         VARCHAR(3) NOT NULL,
    supplier_tier        VARCHAR(30) NULL,
    is_active            BIT NOT NULL
);
GO

CREATE TABLE dbo.carrier_source (
    carrier_id           BIGINT NOT NULL PRIMARY KEY,
    carrier_code         VARCHAR(40) NOT NULL,
    carrier_name         VARCHAR(150) NOT NULL,
    service_level        VARCHAR(50) NULL
);
GO

CREATE TABLE dbo.supply_chain_warehouse_source (
    warehouse_id         BIGINT NOT NULL PRIMARY KEY,
    warehouse_code       VARCHAR(30) NOT NULL,
    warehouse_name       VARCHAR(150) NOT NULL,
    city                 VARCHAR(100) NULL,
    state_code           VARCHAR(10) NULL,
    country_code         VARCHAR(3) NOT NULL
);
GO

CREATE TABLE dbo.purchase_order_source (
    po_id                BIGINT NOT NULL PRIMARY KEY,
    po_number            VARCHAR(60) NOT NULL,
    supplier_id          BIGINT NOT NULL,
    warehouse_id         BIGINT NOT NULL,
    po_status            VARCHAR(30) NOT NULL,
    order_date           DATE NOT NULL,
    expected_date        DATE NULL
);
GO

CREATE TABLE dbo.purchase_order_line_source (
    po_line_id           BIGINT NOT NULL PRIMARY KEY,
    po_id                BIGINT NOT NULL,
    sku                  VARCHAR(50) NOT NULL,
    ordered_qty          INT NOT NULL,
    unit_cost            DECIMAL(12,2) NOT NULL
);
GO

CREATE TABLE dbo.shipment_source (
    shipment_id          BIGINT NOT NULL PRIMARY KEY,
    shipment_number      VARCHAR(60) NOT NULL,
    po_id                BIGINT NOT NULL,
    carrier_id           BIGINT NULL,
    shipment_status      VARCHAR(30) NOT NULL,
    shipped_ts           DATETIME2 NULL,
    eta_ts               DATETIME2 NULL,
    delivered_ts         DATETIME2 NULL
);
GO

CREATE TABLE dbo.shipment_line_source (
    shipment_line_id     BIGINT NOT NULL PRIMARY KEY,
    shipment_id          BIGINT NOT NULL,
    sku                  VARCHAR(50) NOT NULL,
    shipped_qty          INT NOT NULL,
    damaged_qty          INT NOT NULL
);
GO

CREATE TABLE dbo.receiving_event_source (
    receiving_event_id   BIGINT NOT NULL PRIMARY KEY,
    shipment_id          BIGINT NOT NULL,
    warehouse_id         BIGINT NOT NULL,
    sku                  VARCHAR(50) NOT NULL,
    received_qty         INT NOT NULL,
    received_ts          DATETIME2 NOT NULL,
    is_partial           BIT NOT NULL
);
GO
