# Data Dictionary

## AML Case Investigation & SAR Decision Analytics

This data dictionary documents the customer, transaction, investigation-case, case-transaction, and SAR-decision datasets used in the project. It is designed to make the data model, investigation workflow, and analytical fields easy to understand for reviewers of the GitHub portfolio.

> **Portfolio note:** These datasets are used for analytical/portfolio demonstration. Definitions describe how each field functions within this project and are not intended to represent any specific financial institution's production data standard.

## Dataset Overview

| Dataset | Rows | Columns | Purpose |
|---|---:|---:|---|
| `customers(20260914-024810).csv` | 900 | 7 | Customer/KYC reference dataset used to provide customer context for investigations. |
| `transactions(20260914-024811).csv` | 22,000 | 8 | Transaction-level dataset containing activity evaluated during financial-crime investigations. |
| `case_transactions.csv` | 5,095 | 9 | Bridge dataset linking investigation cases to the transactions reviewed within each case. |
| `investigation_cases.csv` | 240 | 23 | Case-level dataset containing investigation attributes, risk context, status, and outcomes. |
| `sar_decisions.csv` | 62 | 12 | Dataset documenting SAR assessment and decision outcomes for investigated cases. |

## `customers(20260914-024810).csv`

Customer/KYC reference dataset used to provide customer context for investigations.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `customer_id` | String | Source / Operational | Unique identifier for the customer. | `CUST10000` |
| `customer_name` | String | Source / Operational | Project field representing customer name. | `Customer 0001` |
| `customer_type` | String | Source / Operational | Category or type of customer. | `Individual` |
| `country` | String | Source / Operational | Country associated with the customer or activity. | `United States` |
| `kyc_risk` | String | Source / Operational | Field used to represent kyc risk in the investigation workflow. | `Low` |
| `pep_flag` | Integer | Source / Operational | Indicator used to identify whether pep applies. | `0` |
| `expected_monthly_volume` | Float | Source / Operational | Project field representing expected monthly volume. | `1358.5` |

## `transactions(20260914-024811).csv`

Transaction-level dataset containing activity evaluated during financial-crime investigations.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `transaction_id` | String | Source / Operational | Unique identifier for the transaction. | `TX300000` |
| `customer_id` | String | Source / Operational | Unique identifier for the customer. | `CUST10217` |
| `transaction_date` | String | Source / Operational | Date on which the transaction occurred. | `2026-08-09` |
| `channel` | String | Source / Operational | Project field representing channel. | `Wire` |
| `direction` | String | Source / Operational | Project field representing direction. | `Credit` |
| `amount` | Float | Source / Operational | Monetary value of the transaction. | `9019.96` |
| `counterparty_country` | String | Source / Operational | Count associated with counterparty country. | `Canada` |
| `high_risk_geo_flag` | Integer | Source / Operational | Indicator used to identify whether high risk geo applies. | `0` |

## `case_transactions.csv`

Bridge dataset linking investigation cases to the transactions reviewed within each case.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `transaction_id` | String | Relationship / Analytical | Unique identifier for the transaction. | `TX313665` |
| `customer_id` | String | Relationship / Analytical | Unique identifier for the customer. | `CUST10180` |
| `transaction_date` | String | Relationship / Analytical | Date on which the transaction occurred. | `2026-03-05` |
| `channel` | String | Relationship / Analytical | Project field representing channel. | `Card` |
| `direction` | String | Relationship / Analytical | Project field representing direction. | `Credit` |
| `amount` | Float | Relationship / Analytical | Monetary value of the transaction. | `486.57` |
| `counterparty_country` | String | Derived / Analytical | Count associated with counterparty country. | `United States` |
| `high_risk_geo_flag` | Integer | Derived / Analytical | Indicator used to identify whether high risk geo applies. | `0` |
| `case_id` | String | Relationship / Analytical | Unique identifier for the investigation case. | `CASE0001` |

## `investigation_cases.csv`

Case-level dataset containing investigation attributes, risk context, status, and outcomes.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `case_id` | String | Source / Operational | Unique identifier for the investigation case. | `CASE0001` |
| `customer_id` | String | Source / Operational | Unique identifier for the customer. | `CUST10180` |
| `case_type` | String | Source / Operational | Classification or typology assigned to the investigation case. | `Unusual Volume Increase` |
| `created_date` | String | Source / Operational | Date associated with created. | `2026-03-27` |
| `lookback_days` | Integer | Derived / Analytical | Project field representing lookback days. | `90` |
| `case_age_days` | Integer | Derived / Analytical | Project field representing case age days. | `1` |
| `reviewed_txn_count` | Integer | Derived / Analytical | Count associated with reviewed txn count. | `99` |
| `reviewed_amount` | Float | Source / Operational | Monetary amount associated with reviewed. | `148832.22` |
| `high_risk_txn_count` | Integer | Derived / Analytical | Count associated with high risk txn count. | `4` |
| `red_flag_count` | Integer | Derived / Analytical | Indicator used to identify whether red count applies. | `2` |
| `primary_red_flag` | String | Derived / Analytical | Indicator used to identify whether primary red applies. | `Unusual Volume` |
| `case_risk_score` | Integer | Derived / Analytical | Numeric score used to represent case risk. | `60` |
| `priority` | String | Source / Operational | Project field representing priority. | `Moderate` |
| `disposition` | String | Source / Operational | Project field representing disposition. | `SAR Filed` |
| `sar_flag` | Integer | Derived / Analytical | Indicator used to identify whether sar applies. | `1` |
| `customer_name` | String | Source / Operational | Project field representing customer name. | `Customer 0181` |
| `customer_type` | String | Source / Operational | Category or type of customer. | `Individual` |
| `country` | String | Derived / Analytical | Country associated with the customer or activity. | `Turkey` |
| `kyc_risk` | String | Source / Operational | Field used to represent kyc risk in the investigation workflow. | `Low` |
| `pep_flag` | Integer | Derived / Analytical | Indicator used to identify whether pep applies. | `0` |
| `expected_monthly_volume` | Float | Source / Operational | Project field representing expected monthly volume. | `7827.87` |
| `investigation_summary` | String | Source / Operational | Project field representing investigation summary. | `Reviewed 99 transactions over a 90-day lookback. Observed unusual volume indicat` |
| `sar_decision_reason` | String | Source / Operational | Project field representing sar decision reason. | `Activity showed multiple unexplained red flags inconsistent with expected custom` |

## `sar_decisions.csv`

Dataset documenting SAR assessment and decision outcomes for investigated cases.

| Column | Data Type | Classification | Description | Example |
|---|---|---|---|---|
| `case_id` | String | Source / Operational | Unique identifier for the investigation case. | `CASE0001` |
| `customer_id` | String | Source / Operational | Unique identifier for the customer. | `CUST10180` |
| `created_date` | String | Source / Operational | Date associated with created. | `2026-03-27` |
| `case_risk_score` | Integer | Derived / Analytical | Numeric score used to represent case risk. | `60` |
| `priority` | String | Source / Operational | Project field representing priority. | `Moderate` |
| `reviewed_amount` | Float | Source / Operational | Monetary amount associated with reviewed. | `148832.22` |
| `primary_red_flag` | String | Derived / Analytical | Indicator used to identify whether primary red applies. | `Unusual Volume` |
| `disposition` | String | Source / Operational | Project field representing disposition. | `SAR Filed` |
| `sar_decision_reason` | String | Source / Operational | Project field representing sar decision reason. | `Activity showed multiple unexplained red flags inconsistent with expected custom` |
| `sar_id` | String | Source / Operational | Unique identifier for the SAR decision or SAR record. | `SAR0001` |
| `sar_status` | String | Source / Operational | Status classification for sar. | `Filed` |
| `filing_date` | String | Source / Operational | Date associated with SAR filing. | `2026-04-01` |

## Dataset Relationships

- `customers(20260914-024810).csv.customer_id` ↔ `transactions(20260914-024811).csv.customer_id` provides a shared key between the two datasets.
- `customers(20260914-024810).csv.customer_id` ↔ `case_transactions.csv.customer_id` provides a shared key between the two datasets.
- `customers(20260914-024810).csv.customer_id` ↔ `investigation_cases.csv.customer_id` provides a shared key between the two datasets.
- `customers(20260914-024810).csv.customer_id` ↔ `sar_decisions.csv.customer_id` provides a shared key between the two datasets.
- `transactions(20260914-024811).csv.transaction_id` ↔ `case_transactions.csv.transaction_id` provides a shared key between the two datasets.
- `transactions(20260914-024811).csv.customer_id` ↔ `case_transactions.csv.customer_id` provides a shared key between the two datasets.
- `transactions(20260914-024811).csv.customer_id` ↔ `investigation_cases.csv.customer_id` provides a shared key between the two datasets.
- `transactions(20260914-024811).csv.customer_id` ↔ `sar_decisions.csv.customer_id` provides a shared key between the two datasets.
- `case_transactions.csv.customer_id` ↔ `investigation_cases.csv.customer_id` provides a shared key between the two datasets.
- `case_transactions.csv.case_id` ↔ `investigation_cases.csv.case_id` provides a shared key between the two datasets.
- `case_transactions.csv.customer_id` ↔ `sar_decisions.csv.customer_id` provides a shared key between the two datasets.
- `case_transactions.csv.case_id` ↔ `sar_decisions.csv.case_id` provides a shared key between the two datasets.
- `investigation_cases.csv.case_id` ↔ `sar_decisions.csv.case_id` provides a shared key between the two datasets.
- `investigation_cases.csv.customer_id` ↔ `sar_decisions.csv.customer_id` provides a shared key between the two datasets.

## Analytical Workflow

**Customer/KYC Context → Transaction Review → Case Investigation → Transaction-to-Case Linkage → SAR Decision**

The structure supports investigation-level analysis by connecting customer context and transactional activity with case outcomes and SAR decisions. This enables analysis of suspicious patterns, investigation workload, case disposition, and SAR decision behavior.

## EDA & Feature Engineering Context

The project data model supports exploratory data analysis across customer, transaction, case, and SAR outcomes. Derived analytical fields can be used to quantify risk, transaction behavior, case complexity, investigation outcomes, and filing patterns. Fields identified as **Derived / Analytical** should be treated as features or metrics created or used for analytical decision support rather than direct source-system attributes.

## Data Quality Conventions

- Identifier fields should be unique within their natural entity tables and validated before joins.
- Transaction monetary fields should be validated for missing, negative, or implausible values according to project business rules.
- Date fields should be standardized before time-based analysis.
- Categorical values should be standardized before aggregation or dashboard reporting.
- Missing values should be interpreted in the context of the field; some may be valid when a decision, closure, or filing event has not occurred.

---

*Prepared for the AML Case Investigation & SAR Decision Analytics GitHub portfolio project.*