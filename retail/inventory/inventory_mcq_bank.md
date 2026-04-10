# 📘 Inventory MCQ Bank

[🏠 Back to Home](../../readme.md)
[📦 Back to Inventory Platform](inventory_full.md)

## 📌 Questions (1-10)
1. Which table should store store-level on-hand and reserved stock?  
A) dim_store  
B) warehouse_inventory  
C) store_inventory  
D) inventory_movement  

2. Which table is best for warehouse stock visibility?  
A) store_inventory  
B) warehouse_inventory  
C) purchase_order  
D) dim_product  

3. Which event should reduce store on-hand quantity?  
A) receive_po  
B) sale  
C) transfer_in  
D) return  

4. Which layer should keep raw incoming files?  
A) Gold  
B) Silver  
C) Bronze  
D) Semantic  

5. Which metric indicates product availability risk?  
A) Stockout rate  
B) CPU utilization  
C) Query count  
D) API key age  

6. What prevents duplicate stock records per product/store?  
A) Random key  
B) Unique `(store_id, product_id)`  
C) Optional index  
D) View only  

7. Which source usually feeds purchase order data?  
A) POS  
B) ERP  
C) Web analytics  
D) Ad platform  

8. What is the role of `inventory_movement`?  
A) Product master only  
B) Captures stock change events  
C) Stores user passwords  
D) Stores BI charts  

9. Why use idempotent processing for movements?  
A) Better UI  
B) Avoid double-counting on replay  
C) Reduce table names  
D) Remove foreign keys  

10. Which output is most useful for replenishment planning?  
A) Net available by location and product  
B) Raw logs only  
C) DDL scripts only  
D) Campaign list  

### ✅ Answer Key
1) C  
2) B  
3) B  
4) C  
5) A  
6) B  
7) B  
8) B  
9) B  
10) A  
