# On Prem - Data Engineering Docker Data Pipelines

## Components
* Document the following in GIT

### Source System
* Source DB (DDL)
* Source API Simulator
  * One API Code for each table
* Source FTP Server
* Data Generators, One for each table
  * CSV Data Generator 
  * Parquet Data Generator
    * Identify industry standard (1 row per file or n rows per file by partition) 
  * Compression/ZIP
  * Check into GIT

## Transformation Layer
### Data Pipeline
* MQ, Kafka
* PySpark
* T-SQL, Pg/PLSQL
* Custom Python Data Pipelines
  * Pandas, Polars, Dask

### Orchestration
* Airflow
* NiFi

## Target System
* Target DW DDL
* Bronze/Gold/Platinum Layer Folder/Table
* No SQL DDL
* Minio Bucket-folder structure
* Data Lake Injestion Layer
  * Icerberg
  * Delta Lake
* No SQL - Mongo DB
* RDBMS - Postgres DB

## Build Process
* All aspects with code
* Terraform
* Python Setup Scripts
