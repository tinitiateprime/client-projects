# 🗺️ Sales Mapping Solution

[🏠 Back to Home](../../readme.md)
[📈 Back to Sales Platform](sales_full.md)

## 📌 Source-to-Target Mapping (Sample)
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| pos | pos_txn_line | sku | dim_product.sku | trim, upper | reject if null |
| pos | pos_txn_line | store_code | dim_store.store_code | trim, upper | reject if null |
| pos | pos_txn_line | qty | fact_sales.quantity | cast int | default 0 |
| pos | pos_txn_line | gross_amt | fact_sales.gross_amount | cast decimal(12,2) | default 0.00 |
| pos | pos_txn_line | discount_amt | fact_sales.discount_amount | cast decimal(12,2) | default 0.00 |
| pos | pos_txn_line | txn_ts | fact_sales.order_ts | parse utc ts | default load ts |
| ecom | order_line | order_line_id | fact_sales.order_line_id | trim | reject if null |
| ecom | order_line | channel | dim_channel.channel_name | normalize vocabulary | default 'web' |
| ecom | order_line | tax_amt | fact_sales.tax_amount | cast decimal(12,2) | default 0.00 |
| returns | return_line | return_reason | fact_returns.return_reason | trim, lower | default 'unknown' |
| promo | promo_event | promo_code | fact_promotion_redemption.promo_code | trim, upper | default 'NA' |

## ✅ Grading Pointers
- Correct dimensional vs fact placement
- Clear transform and null handling
- Coverage across POS, e-commerce, returns, and promotions
