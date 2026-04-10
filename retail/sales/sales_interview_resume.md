# 🎯 Sales Interview Questions and Resume Bullets

[🏠 Back to Home](../../readme.md)
[📈 Back to Sales Platform](sales_full.md)

## 🎯 Interview Q&A
**Q1. What business problem does the Sales platform solve?**  
**A:** It creates one trusted view of sales across POS and e-commerce to drive accurate KPI tracking and decisions.

**Q2. Why do we need both gross and net metrics?**  
**A:** Gross shows topline demand while net captures true revenue after discounts, taxes, and returns.

**Q3. Why track returns separately?**  
**A:** Returns impact revenue and product performance; separate tracking enables root-cause analysis.

**Q4. How do you handle duplicate order lines?**  
**A:** Enforce unique `order_line_id` and idempotent upsert logic during incremental loads.

**Q5. What are critical sales quality checks?**  
**A:** No null keys, positive quantities, valid channel values, and net/gross arithmetic consistency.

**Q6. How do promotions affect modeling?**  
**A:** Promotions are captured in separate redemption facts and linked to sales lines for attribution.

**Q7. What metrics do leadership teams care about?**  
**A:** Net sales, units, margin, return rate, channel mix, and target achievement.

**Q8. How do you scale sales reporting?**  
**A:** Partition by date/channel and pre-aggregate into Gold marts.

## 🎯 Resume Bullets
- Built multi-channel retail sales model covering POS, e-commerce, returns, and promotion attribution.
- Designed Bronze-Silver-Gold pipeline to deliver trusted sales, margin, and target-vs-actual reporting.
- Implemented idempotent order-line processing and quality controls to reduce reporting discrepancies.
- Delivered executive-ready marts for channel performance, product trends, and conversion insights.
