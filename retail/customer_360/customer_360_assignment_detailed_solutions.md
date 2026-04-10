# ✅ Customer 360 Detailed Assignment Solutions

[🏠 Back to Home](../../readme.md)
[🧩 Back to Personalization Platform](customer_360_personalization_platform.md)
## 📌 How To Use This Document
This is an instructor-ready answer key for all 20 Customer 360 assignments.  
Each assignment includes:
- objective
- detailed solution approach
- sample implementation
- expected output
- grading checklist

---

## ✅ Assignment 1: Source-to-Target Mapping
**Objective:** Map POS/CRM/Ecom/Loyalty fields to Customer 360 model with transformations and null/default handling.

**Detailed solution approach:**
1. Identify source entities: customer, contact, address, transactions, interactions.
2. Map identity and profile attributes to `dim_customer`.
3. Map contact details to `dim_customer_email` and `dim_customer_phone`.
4. Map address attributes to `dim_customer_address`.
5. Map orders and events to `fact_transaction` and `fact_customer_interaction`.
6. Define canonical transforms (trim, lowercase, type cast, code map).
7. Define null behavior (reject, default, or generated fallback).

**Sample implementation:**  
Use [customer_360_mapping_solution.md](customer_360_mapping_solution.md) as reference table.

**Expected output:** Complete mapping sheet with source/target/transform/null rules.

**Grading checklist:**
- Covers all systems and core entities
- Uses correct target table
- Includes concrete transforms
- Includes null/default behavior per row

---

## ✅ Assignment 2: Standardize Email and Phone
**Objective:** Standardize contact fields before matching.

**Detailed solution approach:**
1. Email: lowercase + trim + format validation.
2. Phone: remove all non-digits; keep 10 digits for US format.
3. Flag invalid values for DQ reporting.

**Sample SQL:**
```sql
select
  customer_id,
  lower(trim(email_address)) as email_std,
  right(regexp_replace(phone_number, '[^0-9]', '', 'g'), 10) as phone_std
from raw_customer_contact;
```

**Expected output:** Cleaned contact columns (`email_std`, `phone_std`) with high parse success.

**Grading checklist:**
- Handles spaces/case/noise chars
- Produces consistent format
- Captures invalid cases

---

## ✅ Assignment 3: Deterministic Matching
**Objective:** Create exact-match rules using strong identifiers.

**Detailed solution approach:**
1. Match on verified email first.
2. Match on verified phone + DOB second.
3. Assign same `customer_sk` for exact matches.

**Sample SQL pattern:**
```sql
select a.src_id, b.customer_sk
from stg_customer a
join dim_customer_email b
  on lower(trim(a.email)) = lower(trim(b.email_address))
where a.email_verified = true;
```

**Expected output:** Exact-match table with clear matched/unmatched status.

**Grading checklist:**
- Uses strong keys
- Respects verification flags
- Avoids fuzzy logic in deterministic layer

---

## ✅ Assignment 4: Fuzzy Matching and Thresholding
**Objective:** Build score-based matching and classify outcomes.

**Detailed solution approach:**
1. Create features: name similarity, DOB exact, zip exact, phone similarity.
2. Weighted score example: name 35, DOB 25, zip 20, phone 20.
3. Classify:
- `>=0.95`: auto-merge
- `0.80-0.94`: review queue
- `<0.80`: no merge

**Expected output:** Match candidate table with score + decision class.

**Grading checklist:**
- Weighted scoring present
- Threshold bands clearly defined
- Decision labels are deterministic

---

## ✅ Assignment 5: Golden Record + Merge Lineage
**Objective:** Build dedup pipeline with full lineage.

**Detailed solution approach:**
1. Union deterministic and fuzzy outcomes.
2. Choose winning `customer_sk` via survivorship.
3. Persist merge lineage with `match_rule`, `match_score`, `merge_ts`.
4. Publish golden profile table.

**Sample lineage columns:**
`source_customer_id, matched_customer_sk, match_rule, match_score, merge_ts, merged_by_pipeline_run`

**Expected output:** `dim_customer_gold` and `customer_merge_lineage`.

**Grading checklist:**
- Lineage table exists
- Golden table built from resolved identity
- Auditability maintained

---

## ✅ Assignment 6: DDL Constraints and Indexes
**Objective:** Improve dedup quality and performance.

**Detailed solution approach:**
1. Add PK/FK constraints.
2. Add unique index on canonicalized email.
3. Add index on normalized phone and `customer_sk`.
4. Add index on `order_ts` for recent-window queries.

**Expected output:** DDL with constraints and practical indexes.

**Grading checklist:**
- Constraints match model
- Indexes align with query patterns
- No redundant indexing

---

## ✅ Assignment 7: Generate 100,000 Synthetic Records
**Objective:** Produce high-volume test data for all core dimensions.

**Detailed solution approach:**
1. Use Faker with stable seed.
2. Generate one CSV per table.
3. Preserve referential integrity (`customer_id`/`customer_sk` consistency).
4. Validate row counts.

**Expected output:** CSVs with 100k rows each and valid relationships.

**Grading checklist:**
- Exactly 100k rows per required table
- Deterministic generation option
- Clean types and realistic data

---

## ✅ Assignment 8: dbt Models
**Objective:** Build staged, intermediate, and final identity models.

**Detailed solution approach:**
1. `stg_customer`: cleaning and casting.
2. `int_customer_match`: matching rules + score.
3. `dim_customer_gold`: survivorship and final attributes.

**Expected output:** 3 dbt models with clear dependencies and tests.

**Grading checklist:**
- Correct model layering
- Reusable logic
- Test coverage in dbt

---

## ✅ Assignment 9: Data Quality Tests
**Objective:** Add core Silver/Gold data quality checks.

**Detailed solution approach:**
1. Not-null tests (`customer key`, `dob`, `order_id`).
2. Unique tests (`email canonical`, `order_id`).
3. Referential integrity (`fact -> dim`).
4. Threshold-based checks (acceptable null/duplicate rates).

**Expected output:** Automated DQ test suite with pass/fail reporting.

**Grading checklist:**
- Includes all three test categories
- Covers critical columns
- Produces actionable failures

---

## ✅ Assignment 10: Gold Mart for CLV
**Objective:** Build customer lifetime value mart.

**Detailed solution approach:**
1. Aggregate by customer.
2. Compute `order_count`, `lifetime_value`, `last_order_ts`.
3. Include recency bucket for marketing use.

**Sample SQL (concept):**
```sql
select
  customer_sk,
  count(*) as order_count,
  sum(net_amount) as lifetime_value,
  max(order_ts) as last_order_ts
from fact_order
group by 1;
```

**Expected output:** `mart_customer_value`.

**Grading checklist:**
- Correct aggregation grain
- Correct metrics
- Handles null/edge cases

---

## ✅ Assignment 11: Segment Assignment Model
**Objective:** Classify high-value and churn-risk customers.

**Detailed solution approach:**
1. Build RFM-like features.
2. Define rules:
- high_value: high CLV + recent purchases
- churn_risk: low recency + declining frequency
3. Persist segment with version and timestamp.

**Expected output:** `fact_customer_segment` assignments.

**Grading checklist:**
- Segment rules are explicit
- Versioning exists
- Segments are explainable

---

## ✅ Assignment 12: Dashboard Specification
**Objective:** Define business-ready dashboard requirements.

**Detailed solution approach:**
1. Define audience: marketing/CRM analysts.
2. Define KPIs: profile completeness, match rate, duplicate rate, CLV, conversion.
3. Add filters: channel, date range, segment, geography.
4. Define refresh SLA and data owner.

**Expected output:** One-page dashboard spec.

**Grading checklist:**
- KPI definitions clear
- Filters practical
- Governance included

---

## ✅ Assignment 13: CDC + Idempotency
**Objective:** Implement incremental processing safely.

**Detailed solution approach:**
1. Use source watermark (`updated_at` or CDC token).
2. Load only changed records.
3. Use merge/upsert by stable business key.
4. Re-run same batch and verify no duplicate outcome.

**Expected output:** Incremental load design + rerun proof.

**Grading checklist:**
- CDC logic defined
- Idempotent merge logic used
- Re-run validation shown

---

## ✅ Assignment 14: Data Steward Review Queue
**Objective:** Route uncertain matches for manual decision.

**Detailed solution approach:**
1. Capture mid-confidence match candidates.
2. Store both candidate profiles and match evidence.
3. Add decision states: pending/approved/rejected.
4. Feed approved decisions back to model.

**Expected output:** `steward_review_queue` table/process.

**Grading checklist:**
- Includes confidence boundaries
- Captures decision metadata
- Supports feedback loop

---

## ✅ Assignment 15: API-Ready Profile View
**Objective:** Publish one denormalized profile view for consumers.

**Detailed solution approach:**
1. Join customer, primary email, primary phone, primary address.
2. Add behavior features (CLV, last order date, segment).
3. Keep one row per customer.

**Expected output:** `vw_customer_profile_360`.

**Grading checklist:**
- One-row-per-customer enforced
- Includes identity + behavior + segment
- Stable schema for API use

---

## ✅ Assignment 16: Architecture Trade-off Analysis
**Objective:** Compare Data Lake only vs Lake + Postgres warehouse.

**Detailed solution approach:**
1. Compare dimensions: cost, latency, SQL usability, governance, ops effort.
2. Recommend based on team and scale.
3. State decision assumptions.

**Expected output:** Decision matrix + recommendation.

**Grading checklist:**
- Balanced trade-offs
- Context-specific recommendation
- Assumptions explicit

---

## ✅ Assignment 17: PII Protection
**Objective:** Secure sensitive customer attributes.

**Detailed solution approach:**
1. Tokenize SSN; mask email/phone in non-prod.
2. Encrypt data at rest and in transit.
3. Apply RBAC and audit logs.
4. Use least-privilege access patterns.

**Expected output:** PII policy with technical controls.

**Grading checklist:**
- Covers masking/tokenization
- Access controls included
- Auditability included

---

## ✅ Assignment 18: Late-Arriving Data Reconciliation
**Objective:** Handle delayed events without corrupting metrics.

**Detailed solution approach:**
1. Maintain correction window (for example, last 7-14 days).
2. Recompute affected aggregates and segments.
3. Version outputs or stamp correction runs.

**Expected output:** Reconciliation strategy + backfill logic.

**Grading checklist:**
- Windowing strategy clear
- Reprocessing scope bounded
- Downstream correction handled

---

## ✅ Assignment 19: Unit + Integration Testing
**Objective:** Validate both component and pipeline behavior.

**Detailed solution approach:**
1. Unit tests for normalization, scoring, survivorship functions.
2. Integration tests with multi-source sample records.
3. Validate expected merge/no-merge outcomes.

**Expected output:** Test suite with pass criteria and fixtures.

**Grading checklist:**
- Unit and integration both present
- Edge cases included
- Assertions are deterministic

---

## ✅ Assignment 20: Final Project Presentation
**Objective:** Present technical + business outcomes.

**Detailed solution approach:**
1. Show architecture and data flow.
2. Explain identity resolution and dedup strategy.
3. Share DQ, latency, and duplicate reduction metrics.
4. Highlight business impact and future roadmap.

**Expected output:** 8-12 slide final deck.

**Grading checklist:**
- Technical clarity
- Business relevance
- Metrics-backed outcomes
- Clear communication

---

## 📌 Suggested Scoring Framework (Optional)
- 1-5 assignments: 25 points
- 6-10 assignments: 25 points
- 11-15 assignments: 25 points
- 16-20 assignments: 25 points

Pass threshold recommendation: `>= 70/100`.

