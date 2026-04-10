# ✅ Inventory Detailed Assignment Solutions

[🏠 Back to Home](../../readme.md)
[📦 Back to Inventory Platform](inventory_full.md)

## 📌 Detailed Solutions (20 Assignments)
1. Build source-to-target mapping for POS, WMS, ERP, transfer feeds.
Solution: map product/location dimensions first, then movement/PO/transfer facts with transform + null rules.

2. Standardize SKU/location codes.
Solution: `trim`, `upper`, remove special chars, enforce canonical pattern.

3. Create deterministic merge for products.
Solution: unique key on canonical SKU; reject duplicates at Silver load.

4. Create movement classification logic.
Solution: map events to `sale`, `return`, `transfer_in`, `transfer_out`, `receive_po`, `adjustment`.

5. Build current stock snapshot logic.
Solution: aggregate movement deltas by product/location and apply base on-hand.

6. Add DDL constraints/indexes.
Solution: PK/FK, unique `(store_id, product_id)` and `(warehouse_id, product_id)`, index movement timestamp.

7. Generate synthetic inventory data.
Solution: Faker + deterministic seed + referential integrity.

8. Build dbt staging models.
Solution: one staging model per source with clean types and normalized keys.

9. Build dbt intermediate models.
Solution: conformed product/location models + movement standardization.

10. Build dbt marts.
Solution: store availability mart, warehouse availability mart, stockout mart.

11. Define inventory KPIs.
Solution: stock accuracy, stockout rate, days of cover, fill rate, overstock ratio.

12. Build reorder alert logic.
Solution: when available qty < reorder point and recent demand trend supports reorder.

13. Implement incremental loads.
Solution: watermark on event timestamp + idempotent merge/upsert.

14. Handle late events.
Solution: replay by correction window and recalc affected balances.

15. Build transfer SLA tracker.
Solution: compare requested, shipped, received timestamps and statuses.

16. Build purchase order aging report.
Solution: open POs grouped by days since order/expected date.

17. Add data quality suite.
Solution: null, uniqueness, FK integrity, accepted values for movement/status.

18. Add auditability.
Solution: preserve movement-level lineage and reference IDs.

19. Build role-based reporting views.
Solution: store ops view, warehouse ops view, planning view.

20. Final presentation.
Solution: architecture, model, pipeline reliability, and measurable business outcomes.
