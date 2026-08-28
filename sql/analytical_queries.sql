-- ============================================================
-- analytical_queries.sql — Analytical Queries for R1–R5
-- ============================================================

-- ============================================================
-- R1 — Hiring Trends (Temporal Analysis)
-- Question: How do hiring outcomes vary over time?
-- ============================================================
SELECT
    d.year,
    d.month_name,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(
        SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2
    )                           AS hiring_rate_pct
FROM fact_applications f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month_name
ORDER BY d.year, d.month;

-- ============================================================
-- R2 — Technology Analysis
-- Question: Which technologies generate the highest number and
--           proportion of hired candidates?
-- ============================================================
SELECT
    t.technology_name,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(
        SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2
    )                           AS hiring_rate_pct
FROM fact_applications f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hired DESC;

-- ============================================================
-- R3 — Candidate Profile Analysis
-- Question: How do seniority and years of experience affect
--           hiring outcomes?
-- ============================================================
SELECT
    c.seniority,
    CASE
        WHEN c.yoe < 5  THEN '0-4 years'
        WHEN c.yoe < 10 THEN '5-9 years'
        WHEN c.yoe < 20 THEN '10-19 years'
        ELSE                  '20+ years'
    END                         AS experience_range,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(
        SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2
    )                           AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.seniority, experience_range
ORDER BY c.seniority, experience_range;

-- ============================================================
-- R4 — Geographic Analysis
-- Question: Which countries show the highest recruitment activity
--           and how do their hiring outcomes compare?
-- ============================================================
SELECT
    c.country,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(
        SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2
    )                           AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.country
ORDER BY total_applications DESC
LIMIT 20;

-- ============================================================
-- R5 — Assessment Performance Analysis
-- Question: What is the relationship between Code Challenge and
--           Technical Interview scores?
-- ============================================================
SELECT
    a.code_challenge_score,
    a.technical_interview_score,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired
FROM fact_applications f
JOIN dim_assessment a ON f.assessment_key = a.assessment_key
GROUP BY a.code_challenge_score, a.technical_interview_score
ORDER BY a.code_challenge_score, a.technical_interview_score;
