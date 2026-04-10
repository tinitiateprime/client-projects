# 🗺️ Customer 360 Mapping Solution

[🏠 Back to Home](../../readme.md)
[🧩 Back to Personalization Platform](customer_platform.md)
## 📌 Purpose
Reference solution for Assignment 1:
- source column
- target column
- transform rule
- null/default rule

Use this to evaluate student submissions for completeness and correctness.

## 🛍️ POS System Mapping
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| pos | pos_customer | customer_id | dim_customer.customer_id | cast bigint | reject record if null |
| pos | pos_customer | first_name | dim_customer.first_name | trim, initcap | default `'unknown'` |
| pos | pos_customer | middle_name | dim_customer.middle_name | trim, initcap | default `null` |
| pos | pos_customer | last_name | dim_customer.last_name | trim, initcap | default `'unknown'` |
| pos | pos_customer | dob | dim_customer.dob | parse date `yyyy-mm-dd` | default `1900-01-01` |
| pos | pos_customer | gender_code | dim_customer.gender | map `M/F/N/U -> male/female/non_binary/unknown` | default `'unknown'` |
| pos | pos_customer | ssn_last4 | dim_customer.ssn | join with trusted source if full SSN exists, else tokenize placeholder | default `'000-00-0000'` tokenized |
| pos | pos_contact | email | dim_customer_email.email_address | lower, trim | if null generate `unknown+{customer_id}@example.com` |
| pos | pos_contact | phone | dim_customer_phone.phone_number | remove non-digits, keep last 10 | default `'0000000000'` |
| pos | pos_address | addr_line1 | dim_customer_address.address_line_1 | trim, standardize abbreviations | default `'unknown address'` |
| pos | pos_address | addr_line2 | dim_customer_address.address_line_2 | trim | default `null` |
| pos | pos_address | city | dim_customer_address.city | trim, initcap | default `'unknown'` |
| pos | pos_address | state | dim_customer_address.state_code | upper, map to 2-char code | default `'NA'` |
| pos | pos_address | zip | dim_customer_address.postal_code | keep 5/9 digits | default `'00000'` |
| pos | pos_txn | txn_id | fact_transaction.order_id | cast string, prefix `POS-` if needed | reject if null |
| pos | pos_txn | txn_total | fact_transaction.gross_amount | cast decimal(12,2) | default `0.00` |
| pos | pos_txn | discount_total | fact_transaction.discount_amount | cast decimal(12,2) | default `0.00` |
| pos | pos_txn | txn_ts | fact_transaction.transaction_ts | convert to UTC timestamp | default load timestamp |

## 👥 CRM System Mapping
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| crm | crm_customer | party_id | dim_customer.customer_id | map via identity bridge to master key | reject if unresolved |
| crm | crm_customer | given_name | dim_customer.first_name | trim, initcap | default `'unknown'` |
| crm | crm_customer | middle_name | dim_customer.middle_name | trim, initcap | default `null` |
| crm | crm_customer | family_name | dim_customer.last_name | trim, initcap | default `'unknown'` |
| crm | crm_customer | birth_date | dim_customer.dob | parse ISO date | default `1900-01-01` |
| crm | crm_customer | gender | dim_customer.gender | normalize dictionary values | default `'unknown'` |
| crm | crm_pii | ssn_encrypted | dim_customer.ssn | decrypt in secure zone, re-tokenize at rest | default tokenized sentinel |
| crm | crm_email | email_address | dim_customer_email.email_address | lower, trim, validate regex | default generated unknown email |
| crm | crm_email | is_verified | dim_customer_email.is_verified | cast bool | default `false` |
| crm | crm_phone | phone_number | dim_customer_phone.phone_number | digits only | default `'0000000000'` |
| crm | crm_phone | phone_type | dim_customer_phone.phone_type | map to `mobile/home/work` | default `'mobile'` |
| crm | crm_address | line1 | dim_customer_address.address_line_1 | trim | default `'unknown address'` |
| crm | crm_address | line2 | dim_customer_address.address_line_2 | trim | default `null` |
| crm | crm_address | city_name | dim_customer_address.city | trim, initcap | default `'unknown'` |
| crm | crm_address | state_code | dim_customer_address.state_code | upper | default `'NA'` |
| crm | crm_address | postal_code | dim_customer_address.postal_code | normalize postal format | default `'00000'` |
| crm | crm_address | country | dim_customer_address.country_code | map ISO3 | default `'USA'` |

## 🛒 E-commerce System Mapping
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| ecom | ecom_user | user_id | dim_customer.customer_id | identity map to master key | reject if no match and no onboarding rule |
| ecom | ecom_user | first_name | dim_customer.first_name | trim, initcap | default `'unknown'` |
| ecom | ecom_user | last_name | dim_customer.last_name | trim, initcap | default `'unknown'` |
| ecom | ecom_user | email | dim_customer_email.email_address | lower, trim | default generated unknown email |
| ecom | ecom_user | mobile | dim_customer_phone.phone_number | digits only, country normalize | default `'0000000000'` |
| ecom | ecom_order | order_id | fact_transaction.order_id | keep as string unique | reject if null |
| ecom | ecom_order | channel | fact_transaction.channel | hardcode `web` or map source channel | default `'web'` |
| ecom | ecom_order | payment_method | fact_transaction.payment_type | map payment vocabulary | default `'card'` |
| ecom | ecom_order | order_status | fact_transaction.status | map to `completed/refunded/cancelled` | default `'completed'` |
| ecom | ecom_order | order_amount | fact_transaction.gross_amount | cast decimal(12,2) | default `0.00` |
| ecom | ecom_order | promo_discount | fact_transaction.discount_amount | cast decimal(12,2) | default `0.00` |
| ecom | ecom_order | order_created_ts | fact_transaction.transaction_ts | convert timezone to UTC | default load timestamp |
| ecom | web_event | event_type | fact_customer_interaction.interaction_type | map event taxonomy | default `'page_view'` |
| ecom | web_event | event_channel | fact_customer_interaction.channel | normalize to `web/app/email/sms/call_center` | default `'web'` |
| ecom | web_event | campaign_id | fact_customer_interaction.campaign_id | trim, uppercase | default `null` |
| ecom | web_event | event_ts | fact_customer_interaction.interaction_ts | convert to UTC timestamp | default load timestamp |

## 🎁 Loyalty System Mapping
| source_system | source_table | source_column | target_column | transform_rule | null/default_rule |
|---|---|---|---|---|---|
| loyalty | loyalty_member | member_id | dim_customer.customer_id | map via identity table | reject if orphaned |
| loyalty | loyalty_member | first_name | dim_customer.first_name | trim, initcap | default `'unknown'` |
| loyalty | loyalty_member | last_name | dim_customer.last_name | trim, initcap | default `'unknown'` |
| loyalty | loyalty_member | email | dim_customer_email.email_address | lower, trim | default generated unknown email |
| loyalty | loyalty_member | phone | dim_customer_phone.phone_number | digits only | default `'0000000000'` |
| loyalty | loyalty_member | tier_status | dim_customer_interaction.campaign_id | map to pseudo campaign/tier event | default `'TIER_UNKNOWN'` |
| loyalty | loyalty_event | event_name | fact_customer_interaction.interaction_type | normalize event dictionary | default `'loyalty_event'` |
| loyalty | loyalty_event | points_channel | fact_customer_interaction.channel | map to `app/web/store` | default `'app'` |
| loyalty | loyalty_event | event_ts | fact_customer_interaction.interaction_ts | parse timestamp UTC | default load timestamp |

## ✅ Grading Rubric (Quick Check)
Use this rubric to score students (100 points):
- Mapping coverage (all major entities and systems): 30
- Correct target model usage (dim vs fact): 20
- Transform rule quality (normalization, type casting, code mapping): 20
- Null/default rule quality and data safety: 20
- Clarity and documentation format: 10

## ✅ Minimum Expected Deliverables From Students
- At least 30 mapping rows across POS/CRM/Ecom.
- Explicit transform rule per row.
- Explicit null/default handling per row.
- Correct placement into `dim_customer`, contact dims, and fact tables.


