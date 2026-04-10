# 🗺️ Supply Chain Mapping Solution

[🏠 Back to Home](../../readme.md)
[🚚 Back to Supply Chain Platform](supply_chain_full.md)

## 📌 Source-to-Target Mapping (Sample)
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| erp | po_header | po_num | purchase_order.po_number | trim, upper | reject if null |
| erp | po_header | supplier_code | dim_supplier.supplier_code | trim, upper | reject if null |
| erp | po_header | wh_code | dim_warehouse.warehouse_code | trim, upper | reject if null |
| erp | po_line | sku | purchase_order_line.sku | trim, upper | reject if null |
| tms | shipment | shipment_no | shipment.shipment_number | trim, upper | reject if null |
| tms | shipment | status | shipment.shipment_status | normalize values | default 'created' |
| wms | receiving | received_qty | receiving_event.received_qty | cast int | default 0 |
| wms | receiving | received_ts | receiving_event.received_ts | parse utc ts | default load ts |

## ✅ Grading Pointers
- Correct table mapping
- Explicit transform rule
- Explicit null/default handling
