# 📘 Supply Chain MCQ Bank

[🏠 Back to Home](../../readme.md)
[🚚 Back to Supply Chain Platform](supply_chain_full.md)

## 📌 Questions (1-10)
1. Which table tracks shipment header status?
A) purchase_order_line
B) shipment
C) receiving_event
D) dim_supplier

2. Which KPI measures delivery punctuality?
A) Fill rate
B) On-time delivery
C) Unit cost
D) Revenue growth

3. Which source typically provides PO data?
A) ERP
B) CRM
C) POS
D) CMS

4. Partial deliveries should be captured in:
A) dim_carrier
B) receiving_event
C) dim_warehouse
D) fact_sales

5. Which layer stores raw source feeds?
A) Bronze
B) Silver
C) Gold
D) Semantic

6. Which field best links shipment lines to planning context?
A) supplier_name
B) shipment_number
C) movement_ts
D) city

7. Which quality check is most critical for shipment facts?
A) Image size check
B) Duplicate shipment number check
C) Font check
D) Color check

8. Lead time is generally calculated from:
A) delivered_ts - order_date
B) created_at - eta_ts
C) updated_at - order_ts
D) received_ts - shipped_qty

9. Why model supplier dimension?
A) For UI themes
B) For supplier performance analytics
C) To replace shipment table
D) To remove keys

10. Idempotent ingestion helps by:
A) Increasing delays
B) Preventing duplicate processing
C) Removing timestamps
D) Hiding errors

### ✅ Answer Key
1) B
2) B
3) A
4) B
5) A
6) B
7) B
8) A
9) B
10) B
