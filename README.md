# FraudDetection
An end-to-end machine learning project for fraud detection in financial transactions.

[Executive Summary]

**Fraud Analysis Dashboard:** https://public.tableau.com/app/profile/pablo.tikas.pueyo/viz/FraudDashboard_17748659627020/Dashboard1


## Data source
**Financial Transactions Dataset: Analytics (Kaggle)**

*This comprehensive financial dataset created by Caixabank Tech for the 2024 AI Hackathon combines transaction records, customer information, and card data from a banking institution, spanning across the 2010s decade. The dataset is designed for multiple analytical purposes, including synthetic fraud detection, customer behavior analysis, and expense forecasting.*

https://www.kaggle.com/datasets/computingvictor/transactions-fraud-datasets

## Phase 1: Exploratory Data Analysis

### Phase Goals

- Develop a deep understanding of the dataset: fields in each table, relationships between fields, number of records, number of nulls, etc.
- Create an exhaustive report on the raw dataset.
- Create an insightful, interactive dashboard.

### Tech Stack

- **DBeaver** for database management + SQL queries.
- **Tableau Public** for data visualization.

### Phase Journal

**24th of March, 2026**
- Downloaded the Kaggle dataset.
- Created a new database in DBeaver and uploaded all the CSV files.
- Processed "train_fraud_labels.json" with Python and created a csv with binary labels.
- Uploaded the new CSV with binary training labels to DBeaver.

**26th of March, 2026**
- Wrote the "RawDataReport.md", using database schema and SQL queries (*sql/RawDataReport.sql*).
- Executed SQL queries to prepare for EDA phase (*sql/EDA.sql*).
- Created an initial design for the Fraud Analytics dashboard.

**30th of March, 2026**
- Finalized *Fraud Analytics Dashboard*, including multiple charts, tables, KPIs, and global filters.


## Phase 2: Modeling & Experimentation.

### Phase Goals

### Tech Stack

### Phase Journal
