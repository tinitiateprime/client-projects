# 🎯 Customer 360 Interview Questions and Resume Bullets

[🏠 Back to Home](../../readme.md)
[🧩 Back to Personalization Platform](customer_platform.md)

## 🎯 How to present this project
Use this project when the role expects:
- customer analytics
- master data / conformed dimensions
- marketing or personalization support
- data platform leadership
- cross-channel retail reporting

## 🎯 Strong interview answer
> I led the design of a Customer 360 platform that consolidated POS, e-commerce, CRM, and loyalty data into a unified retail customer profile. We landed raw data in Bronze, standardized and matched identities in Silver, and built Gold-layer customer profile and segmentation datasets for dashboards and personalization use cases. A key part of the solution was deduplication, customer key assignment, and making the pipeline idempotent so reprocessing never created duplicate records.

## 🎯 Interview Q&A Bank
**Q1. What problem does Customer 360 solve?**  
**A:** It solves fragmented customer data across POS, CRM, e-commerce, and loyalty systems. The outcome is one trusted profile per customer for analytics, personalization, and campaign activation.

**Q2. How did you design Bronze, Silver, and Gold layers?**  
**A:** Bronze stores raw immutable source files in S3. Silver standardizes and cleanses data, performs identity resolution, and enforces quality checks in Postgres. Gold provides business-ready marts for BI, segmentation, and personalization APIs.

**Q3. How did you remove duplicate customer records?**  
**A:** I used deterministic matching first (SSN, verified email, verified phone + DOB), then probabilistic scoring for weaker matches. Records above confidence threshold auto-merge, mid-range go to steward review, and low-confidence remain separate.

**Q4. What survivorship logic did you apply for the golden record?**  
**A:** I prioritized verified and most recent values with source precedence rules, such as CRM over web form for identity attributes. I also stored lineage metadata so every merged value is auditable.

**Q5. How did you handle incremental loads and idempotency?**  
**A:** I used watermark-based ingestion and upsert/merge logic with stable business keys. Reprocessing the same batch does not create duplicates because dedup and merge rules are deterministic.

**Q6. Which data quality checks were most important?**  
**A:** Null checks on key identifiers, format checks for email/phone/DOB, uniqueness checks on canonicalized email, and referential integrity checks between customer dimension and fact tables.

**Q7. Why did you choose Postgres for Silver/Gold in one architecture option?**  
**A:** Postgres gave strong relational modeling, constraints, and simple operational querying for downstream BI teams. It was a good fit for moderate-scale conformed marts with frequent business reporting.

**Q8. How did this platform improve business outcomes?**  
**A:** It improved match accuracy, reduced duplicate profiles, increased campaign precision, and gave marketing and analytics teams a consistent customer definition, which improved retention-focused decision making.

**Q9. What metrics did you track to prove success?**  
**A:** Match rate, duplicate rate, golden-record completeness, pipeline SLA adherence, reporting freshness, and campaign lift metrics like conversion and repeat purchase rate.

**Q10. How did you support downstream personalization use cases?**  
**A:** I published Gold datasets with profile, behavior, and segment features, then exposed them to BI and API consumers. This enabled near-real-time audience selection and recommendation workflows.

**Q11. What were the hardest technical challenges?**  
**A:** Cross-system identity conflicts and inconsistent source quality. The key was combining robust standardization, rule-based matching, and stewardship workflows with clear auditability.

**Q12. If you had to scale this to 10x data, what would you change?**  
**A:** I would move more matching and transformation workloads to distributed compute, partition heavily by ingestion date and source, and optimize serving patterns with materialized marts and asynchronous feature refresh.

## 🎯 Resume Bullet Ideas
- Led delivery of a retail Customer 360 data platform integrating POS, CRM, e-commerce, and loyalty data into a unified analytics-ready model.
- Designed Bronze, Silver, and Gold data layers to support customer profiling, segmentation, and personalization use cases.
- Implemented identity resolution and master customer key mapping to improve customer match accuracy across channels.
- Enabled BI and downstream marketing activation through curated Gold-layer datasets and reusable dimensional models.

