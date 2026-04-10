# 📘 Customer 360 MCQ Bank

[🏠 Back to Home](../../readme.md)
[🧩 Back to Personalization Platform](customer_360_personalization_platform.md)
## 📌 MCQ Test (Set 1: Questions 1-10)
1. Which layer should store immutable raw source files?  
A) Gold  
B) Silver  
C) Bronze  
D) Semantic  

2. Which is a deterministic match rule?  
A) Similar last name and same city  
B) Same verified email address  
C) Similar first name and zip  
D) Same device type  

3. Which table is best for storing multiple phone records per customer?  
A) fact_order  
B) dim_customer_phone  
C) dim_customer  
D) fact_customer_interaction  

4. What is survivorship in Customer 360?  
A) Deleting all old records  
B) Choosing best attribute values for golden record  
C) Archiving Bronze tables  
D) Creating BI dashboards  

5. Which metric best indicates duplicate reduction effectiveness?  
A) Query runtime  
B) Duplicate rate  
C) Number of dashboards  
D) File size growth  

6. In a Data Lake + Warehouse setup, Silver is commonly implemented in:  
A) Redis  
B) Postgres  
C) Excel  
D) Kafka topics only  

7. Why use idempotent pipelines?  
A) To increase UI colors  
B) To prevent duplicate outputs on reprocessing  
C) To avoid creating dimensions  
D) To disable quality checks  

8. Which field is most sensitive and should be protected as PII?  
A) Campaign ID  
B) Channel  
C) SSN  
D) Segment version  

9. What should happen to records with mid-confidence fuzzy match scores?  
A) Auto-delete  
B) Auto-merge always  
C) Send to steward review queue  
D) Ignore permanently  

10. Which Gold-layer output is most useful for personalization?  
A) Raw source file logs  
B) Unified customer profile + segment features  
C) Temporary ingestion errors  
D) DDL scripts only  

### ✅ Set 1 Answer Key
1) C  
2) B  
3) B  
4) B  
5) B  
6) B  
7) B  
8) C  
9) C  
10) B  

---

## 📌 MCQ Test (Set 2: Questions 11-20)
11. Which key design helps avoid duplicate inserts during reruns?  
A) Random UUID per run  
B) Idempotent upsert with business key  
C) Daily table truncate  
D) Manual file renaming  

12. Which layer should contain conformed and standardized customer records?  
A) Bronze  
B) Silver  
C) Gold  
D) Source  

13. A good blocking key for candidate matching is:  
A) Transaction amount only  
B) Last login timestamp  
C) Email or phone + last name  
D) Campaign ID  

14. What is the main purpose of a merge lineage table?  
A) Store UI themes  
B) Track how and why records were merged  
C) Replace all source tables  
D) Increase file compression  

15. Which operation is most appropriate for loading dimension updates?  
A) DROP TABLE  
B) MERGE/UPSERT  
C) DELETE ALL + INSERT  
D) RANDOM SAMPLE  

16. What is a primary benefit of Gold marts?  
A) Raw replay storage  
B) Faster business reporting and reusable KPIs  
C) Source system backup replacement  
D) Removing governance  

17. Which check validates relationship quality between facts and dimensions?  
A) Regex check  
B) Null check  
C) Referential integrity check  
D) Percentile check  

18. In duplicate resolution, what should low-confidence matches do?  
A) Auto-merge  
B) Be ignored from pipeline forever  
C) Stay separate until more evidence arrives  
D) Replace master record  

19. Which data should generally be masked in non-production?  
A) Product category  
B) SSN and personal contacts  
C) Campaign names  
D) Country code  

20. Which outcome best indicates Customer 360 success?  
A) More source systems without governance  
B) Higher duplicate count  
C) Better targeting and improved retention metrics  
D) Longer ETL scripts  

### ✅ Set 2 Answer Key
11) B  
12) B  
13) C  
14) B  
15) B  
16) B  
17) C  
18) C  
19) B  
20) C  

