-- Sales source-side ingestion objects for SQL Server
-- These tables represent source feeds that can be loaded into the sales target model.

IF OBJECT_ID('dbo.sales_calendar_source', 'U') IS NOT NULL DROP TABLE dbo.sales_calendar_source;
GO
IF OBJECT_ID('dbo.product_master_source', 'U') IS NOT NULL DROP TABLE dbo.product_master_source;
GO
IF OBJECT_ID('dbo.store_master_source', 'U') IS NOT NULL DROP TABLE dbo.store_master_source;
GO
IF OBJECT_ID('dbo.channel_master_source', 'U') IS NOT NULL DROP TABLE dbo.channel_master_source;
GO
IF OBJECT_ID('dbo.pos_txn_line_source', 'U') IS NOT NULL DROP TABLE dbo.pos_txn_line_source;
GO
IF OBJECT_ID('dbo.ecom_order_line_source', 'U') IS NOT NULL DROP TABLE dbo.ecom_order_line_source;
GO
IF OBJECT_ID('dbo.return_line_source', 'U') IS NOT NULL DROP TABLE dbo.return_line_source;
GO
IF OBJECT_ID('dbo.promo_event_source', 'U') IS NOT NULL DROP TABLE dbo.promo_event_source;
GO
IF OBJECT_ID('dbo.sales_target_plan_source', 'U') IS NOT NULL DROP TABLE dbo.sales_target_plan_source;
GO

CREATE TABLE dbo.sales_calendar_source (
    date_key             INT PRIMARY KEY,
    full_date            DATE NOT NULL,
    day_of_week          INT NULL,
    month_num            INT NULL,
    quarter_num          INT NULL,
    year_num             INT NULL
);
GO

CREATE TABLE dbo.product_master_source (
    product_id           BIGINT NOT NULL PRIMARY KEY,
    sku                  VARCHAR(50) NOT NULL,
    product_name         VARCHAR(200) NOT NULL,
    category             VARCHAR(100) NULL,
    brand                VARCHAR(100) NULL
);
GO

CREATE TABLE dbo.store_master_source (
    store_id             BIGINT NOT NULL PRIMARY KEY,
    store_code           VARCHAR(30) NOT NULL,
    store_name           VARCHAR(150) NOT NULL,
    city                 VARCHAR(100) NULL,
    state_code           VARCHAR(10) NULL,
    country_code         VARCHAR(3) NOT NULL
);
GO

CREATE TABLE dbo.channel_master_source (
    channel_id           BIGINT NOT NULL PRIMARY KEY,
    channel_name         VARCHAR(50) NOT NULL
);
GO

CREATE TABLE dbo.pos_txn_line_source (
    txn_line_id          VARCHAR(80) NOT NULL PRIMARY KEY,
    order_id             VARCHAR(60) NOT NULL,
    sku                  VARCHAR(50) NOT NULL,
    store_code           VARCHAR(30) NOT NULL,
    city                 VARCHAR(100) NULL,
    state_code           VARCHAR(10) NULL,
    qty                  INT NOT NULL,
    gross_amt            DECIMAL(12,2) NOT NULL,
    discount_amt         DECIMAL(12,2) NOT NULL,
    txn_ts               DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.ecom_order_line_source (
    order_line_id        VARCHAR(80) NOT NULL PRIMARY KEY,
    order_id             VARCHAR(60) NOT NULL,
    sku                  VARCHAR(50) NOT NULL,
    channel              VARCHAR(50) NOT NULL,
    qty                  INT NOT NULL,
    gross_amt            DECIMAL(12,2) NOT NULL,
    discount_amt         DECIMAL(12,2) NOT NULL,
    tax_amt              DECIMAL(12,2) NOT NULL,
    order_ts             DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.return_line_source (
    return_id            VARCHAR(80) NOT NULL PRIMARY KEY,
    order_line_id        VARCHAR(80) NOT NULL,
    return_reason        VARCHAR(100) NULL,
    return_qty           INT NOT NULL,
    return_amount        DECIMAL(12,2) NOT NULL,
    return_ts            DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.promo_event_source (
    promo_event_id       VARCHAR(80) NOT NULL PRIMARY KEY,
    order_id             VARCHAR(60) NOT NULL,
    promo_code           VARCHAR(60) NOT NULL,
    promo_channel        VARCHAR(30) NULL,
    discount_value       DECIMAL(12,2) NOT NULL,
    event_ts             DATETIME2 NOT NULL
);
GO

CREATE TABLE dbo.sales_target_plan_source (
    target_id            VARCHAR(80) NOT NULL PRIMARY KEY,
    date_key             INT NOT NULL,
    store_id             BIGINT NULL,
    channel_id           BIGINT NOT NULL,
    target_net_sales     DECIMAL(14,2) NOT NULL,
    target_units         INT NOT NULL
);
GO
