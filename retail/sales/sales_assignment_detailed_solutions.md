# ✅ Sales Detailed Assignment Solutions

[🏠 Back to Home](../../readme.md)
[📈 Back to Sales Platform](sales_full.md)

## 📌 Detailed Solutions (20 Assignments)
1. Build POS + e-commerce source-to-target mapping.  
Solution: map product/store/channel dims first, then sales/returns/promo facts with explicit transforms.

2. Standardize SKU, channel, and order identifiers.  
Solution: trim/uppercase canonical keys and enforce unique order-line IDs.

3. Implement gross/net/tax consistency checks.  
Solution: assert `net = gross - discount + tax`.

4. Build deterministic order dedup logic.  
Solution: unique key on `order_line_id`, idempotent merge.

5. Model returns impact on sales KPIs.  
Solution: link `fact_returns` to `fact_sales` and compute net-realized sales.

6. Create DDL constraints and indexes.  
Solution: PK/FK, unique constraints, indexes on date/channel/store/product.

7. Generate 100k synthetic sales records.  
Solution: Faker + realistic amount distributions and channels.

8. Build staging models in dbt.  
Solution: one staging model per source with cleaned column types.

9. Build intermediate conformed models.  
Solution: conformed dimensions and sales event normalization.

10. Build Gold channel-performance mart.  
Solution: aggregate net sales/units/margin by date/channel.

11. Build product-performance mart.  
Solution: SKU-level trend, sell-through, margin.

12. Build store-performance mart.  
Solution: target vs actual by store/day/week/month.

13. Add incremental load logic.  
Solution: watermark by `order_ts` with rerun-safe merge.

14. Add late-arriving order reconciliation.  
Solution: backfill window and aggregate refresh for affected periods.

15. Add promotion impact analysis.  
Solution: promo redemption join with sales and uplift metrics.

16. Add data quality suite.  
Solution: null checks, duplicate checks, FK checks, accepted values.

17. Add sales target variance logic.  
Solution: compute absolute and percentage variance.

18. Add role-based reporting views.  
Solution: finance, merchandising, and store-ops specific marts/views.

19. Add lineage and auditability.  
Solution: source file ID, ingestion timestamp, and pipeline run ID tracking.

20. Final presentation.  
Solution: architecture, key models, quality metrics, and business outcomes.
