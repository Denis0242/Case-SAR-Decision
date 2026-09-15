# AML Case Investigation & SAR Decision Analytics

**Financial Crime Analytics Portfolio Project**

An end-to-end AML investigation project using **Python, SQL, Tableau,
and Streamlit** to connect customer/KYC context, transaction lookback
analysis, investigation red flags, case prioritization, disposition
outcomes, and SAR decision support.


------------------------------------------------------------------------

## Analytical Workflow

``` text
Customer / KYC Context
        ↓
Transaction Review
        ↓
Escalated Investigation Case
        ↓
Transaction Lookback
        ↓
Red-Flag & Risk Analysis
        ↓
Investigation Summary
        ↓
Case Disposition
        ↓
SAR Recommendation / Filing Decision
        ↓
Portfolio & Executive Reporting
```

------------------------------------------------------------------------

## Executive Dashboard

![AML Case Investigation & SAR Decision Analytics — Executive Dashboard](images/02_executive_dashboard.png)

The Executive Dashboard summarizes the current processed-data results, including **240 total cases, 128 High/Critical cases, 62 SAR decisions, 35 SAR filings, 62 cases escalated for additional review, and $23.5M in reviewed amount**.

------------------------------------------------------------------------

## Tools & Technologies

  -----------------------------------------------------------------------
  Tool                                Use
  ----------------------------------- -----------------------------------
  **Python / Pandas**                 EDA, validation, feature
                                      engineering and case analysis

  **SQL**                             Investigation queues, aging, red
                                      flags, lookback and SAR analysis

  **Tableau**                         Executive investigation dashboard

  **Streamlit**                       Case 360, transaction lookback and
                                      decision support

  **Jupyter Notebook**                Reproducible analysis

  **Git / GitHub**                    Version control and portfolio
                                      presentation
  -----------------------------------------------------------------------

<<<<<<< HEAD

=======
------------------------------------------------------------------------

## Repository Structure

``` text
Case-SAR-Decision/
├── app/             # Streamlit investigation application
├── data/            # Raw and processed synthetic datasets
├── docs/            # Data dictionary and supporting documentation
├── images/          # Executive dashboard image
├── notebooks/       # Python EDA, feature engineering and investigation analysis
├── sql/             # Investigation and SAR analysis queries
├── tableau/         # Tableau workbook / assets if included
├── .gitignore
├── .python-version
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

------------------------------------------------------------------------

## How to Run

``` bash
git clone https://github.com/Denis0242/Case-SAR-Decision.git
cd Case-SAR-Decision
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

------------------------------------------------------------------------

## Skills Demonstrated

### AML / Financial Crime

-   AML Case Investigation
-   Transaction Lookback Analysis
-   KYC Context Review
-   Red-Flag Identification
-   Case Risk Assessment
-   Investigation Prioritization
-   Case Disposition Analysis
-   SAR Decision Analytics
-   Investigation Narrative Review
-   Financial Crime Decision Support

### Data & Analytics

-   Exploratory Data Analysis
-   Data Quality Validation
-   Feature Engineering
-   SQL Analysis
-   Python / Pandas
-   KPI Development
-   Risk Segmentation
-   Pattern & Trend Analysis
-   Case-Level Analytics

### Reporting & Visualization

-   Tableau
-   Streamlit
-   Case 360 Reporting
-   Executive KPI Reporting
-   Interactive Analytics
-   Data Storytelling

------------------------------------------------------------------------
>>>>>>> e8b4f44 (Make changes to the Readme and Streamlit)

## Disclaimer

This project uses **synthetic data** created for educational and
portfolio purposes. No real customer, account, transaction,
investigation case, SAR, analyst, or confidential financial-institution
data is included.

<<<<<<< HEAD

=======
Case-risk scores, red flags, investigation summaries, dispositions, SAR
recommendations, filing decisions, and analytical thresholds are
illustrative. They demonstrate AML investigation and financial-crime
analytics workflows and should not be interpreted as actual bank
policies, regulatory determinations, or regulatory filings.
>>>>>>> e8b4f44 (Make changes to the Readme and Streamlit)
