# 🗺️ Inventory Mapping Solution

[🏠 Back to Home](../../readme.md)
[📦 Back to Inventory Platform](inventory_full.md)

## 📌 Source-to-Target Mapping (Sample Solution)
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| pos | pos_sale_line | sku | dim_product.sku | trim, upper | reject if null |
| pos | pos_sale_line | qty_sold | inventory_movement.quantity | cast int, abs | default 0 |
| pos | pos_sale_line | sale_ts | inventory_movement.movement_ts | parse utc ts | default load ts |
| pos | pos_sale_line | store_code | dim_store.store_code | trim, upper | reject if null |
| wms | wms_stock | wh_code | dim_warehouse.warehouse_code | trim, upper | reject if null |
| wms | wms_stock | on_hand | warehouse_inventory.on_hand_qty | cast int | default 0 |
| wms | wms_stock | allocated | warehouse_inventory.allocated_qty | cast int | default 0 |
| erp | po_header | po_num | purchase_order.po_number | trim, upper | reject if null |
| erp | po_line | ordered_qty | purchase_order_line.ordered_qty | cast int | default 0 |
| transfer | transfer_hdr | transfer_no | stock_transfer.transfer_number | trim, upper | reject if null |
| transfer | transfer_line | shipped_qty | stock_transfer_line.shipped_qty | cast int | default 0 |

## ✅ Grading Pointers
- Correct table assignment (dim vs fact/operational)
- Explicit transform rules
- Explicit null/default behavior
- Coverage across POS/WMS/ERP/transfer systems
