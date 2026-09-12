-- AML Case Investigation & SAR Decision Analytics

-- 1. Investigator priority queue
SELECT *
FROM investigation_cases
ORDER BY case_risk_score DESC, case_age_days DESC;

-- 2. High / critical cases
SELECT *
FROM investigation_cases
WHERE priority IN ('High','Critical')
ORDER BY case_risk_score DESC;

-- 3. SAR recommended or filed
SELECT *
FROM investigation_cases
WHERE sar_flag = 1
ORDER BY case_risk_score DESC;

-- 4. Cases requiring additional review
SELECT *
FROM investigation_cases
WHERE disposition = 'Escalate for Additional Review'
ORDER BY case_age_days DESC;

-- 5. Case aging
SELECT priority,
       AVG(case_age_days) AS avg_case_age,
       MAX(case_age_days) AS max_case_age
FROM investigation_cases
GROUP BY priority;

-- 6. SAR conversion by case type
SELECT case_type,
       COUNT(*) AS cases,
       SUM(sar_flag) AS sar_cases,
       1.0 * SUM(sar_flag) / COUNT(*) AS sar_conversion_rate
FROM investigation_cases
GROUP BY case_type
ORDER BY sar_conversion_rate DESC;

-- 7. Red-flag distribution
SELECT primary_red_flag, COUNT(*) AS cases
FROM investigation_cases
GROUP BY primary_red_flag
ORDER BY cases DESC;

-- 8. PEP / high-KYC-risk cases
SELECT *
FROM investigation_cases
WHERE pep_flag = 1 OR kyc_risk = 'High'
ORDER BY case_risk_score DESC;

-- 9. Lookback analysis
SELECT lookback_days,
       COUNT(*) AS cases,
       AVG(reviewed_txn_count) AS avg_transactions_reviewed,
       AVG(reviewed_amount) AS avg_reviewed_amount
FROM investigation_cases
GROUP BY lookback_days
ORDER BY lookback_days;

-- 10. Reviewed amount and risk
SELECT case_id, customer_id, reviewed_amount, case_risk_score, red_flag_count, disposition
FROM investigation_cases
ORDER BY reviewed_amount DESC;

-- 11. Monthly case trend
SELECT DATE_TRUNC('month', created_date) AS month,
       COUNT(*) AS cases,
       SUM(sar_flag) AS sar_cases
FROM investigation_cases
GROUP BY DATE_TRUNC('month', created_date)
ORDER BY month;

-- 12. SAR filing queue
SELECT *
FROM sar_decisions
WHERE sar_status IN ('Recommended','Filed')
ORDER BY case_risk_score DESC;
