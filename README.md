# AML Case Investigation & SAR Decision Analytics

Project 5 in the Financial Crime Analytics portfolio.

This project is intentionally different from Project 1. Project 1 focuses on transaction-monitoring alerts. Project 5 begins after an alert has been escalated into an investigation case.

## Scale
- 900 synthetic customers
- 22,000 synthetic transactions
- 240 investigation cases
- 62 SAR recommendations / filing decisions

## Workflow
Escalated alert → case creation → KYC review → transaction lookback → red-flag analysis → investigation summary → disposition → SAR decision.

## Tools
SQL, Python, Tableau, Streamlit.

## Separate KPI Visualization
The project includes a standalone KPI scorecard:
1. Total Cases
2. High/Critical Cases
3. SAR Decisions
4. SAR Filed
5. Additional Review
6. Reviewed Amount

## Executive Dashboard
Exactly six analytical visualizations:
1. Case & SAR Trends
2. Case Disposition donut
3. Top Investigation Red Flags
4. Case Aging Heatmap with numbers inside cells
5. Reviewed Amount vs Case Risk scatter
6. SAR Conversion by Case Type

The final approved dashboard uses one visualization color only: blue, with lighter and darker blue shades where separation is required. Dates use MM/YY such as 07/26.

## Resume Bullets
**AML Case Investigation & SAR Decision Analytics | SQL, Python, Tableau, Streamlit**
- Built an end-to-end AML case-investigation analytics project across 240 synthetic cases, combining KYC context, transaction lookback analysis, red-flag indicators, case-risk scoring, investigation summaries, and SAR decision support.
- Developed SQL investigation queries and Tableau/Streamlit reporting for case prioritization, aging, SAR conversion, escalation monitoring, and reviewed transaction exposure.

## Interview Explanation
“I built this project to simulate the stage after an AML alert is escalated into a case. I reviewed customer KYC context and transaction activity over defined lookback periods, analyzed red flags, created an explainable case-risk score, documented the investigation outcome, and tracked whether the case was closed, escalated further, or moved to SAR consideration. SQL supports the investigation logic, Python prepares and analyzes the data, Tableau shows management trends, and Streamlit provides an investigator-style case review workflow.”

## Disclaimer
All customers, transactions, investigation cases, notes, and SAR decisions are synthetic and created for educational portfolio use only.


## Approved Final Dashboard
Project 5 now uses the approved single-blue dashboard design. It contains six KPI cards and exactly six analytical visualizations. The packaged `images/02_executive_dashboard.png` is the final visual reference.
