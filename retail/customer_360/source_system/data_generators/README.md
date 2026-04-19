# Customer 360 Data Generators

The generator emits zipped source files for source-system ingestion. It supports CSV and Snappy parquet outputs.

Parquet files use the standard high-volume layout of multiple row chunks per zip. The default chunk size is 250,000 rows per parquet file and can be changed with `--parquet-rows-per-file`.

```powershell
python .\customer_360_source_generators.py --output-dir ..\generated
```
