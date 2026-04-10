# 🎯 Inventory Interview Questions and Resume Bullets

[🏠 Back to Home](../../readme.md)
[📦 Back to Inventory Platform](inventory_full.md)

## 🎯 Interview Q&A
**Q1. What is the objective of an Inventory 360 platform?**  
**A:** Provide one trusted inventory view across store and warehouse locations for accurate replenishment and reporting.

**Q2. Why separate store and warehouse inventory tables?**  
**A:** Their operational behaviors differ (reserved/allocated/in-transit), so separate tables improve clarity and query performance.

**Q3. How do you avoid negative inventory?**  
**A:** Use transaction-level validation, movement controls, and guardrail checks before committing stock decrements.

**Q4. What is the role of `inventory_movement`?**  
**A:** It is the event/audit table capturing every stock change with reason and reference.

**Q5. How do you support real-time inventory updates?**  
**A:** Consume source events, apply idempotent movement processing, and update current balance tables.

**Q6. Which metrics prove solution quality?**  
**A:** Stock accuracy %, stockout rate, overstock %, fill rate, transfer cycle time, and reconciliation drift.

**Q7. How do you handle late-arriving events?**  
**A:** Replay with event timestamps and re-reconcile affected balances by product/location windows.

**Q8. Why use Gold marts?**  
**A:** They provide curated business metrics for planners, store ops, and supply-chain reporting.

**Q9. What quality checks are critical?**  
**A:** No null keys, no duplicate movement IDs, valid movement types, and FK integrity across dimension keys.

**Q10. What scaling improvements would you apply at 10x volume?**  
**A:** Partition movement data by date/location, incremental materialization, and optimized summary tables.

## 🎯 Resume Bullets
- Built a multi-location inventory platform spanning store and warehouse stock visibility with real-time movement tracking.
- Designed conformed inventory model with location-level balances, movement lineage, and replenishment-ready metrics.
- Implemented idempotent inventory movement processing to prevent double-counting during replay and retries.
- Delivered Gold-layer inventory marts for stockout monitoring, net-available reporting, and replenishment decisions.
