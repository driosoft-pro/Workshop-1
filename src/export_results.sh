#!/usr/bin/env bash
# export_results.sh — Export analytical query results to CSV.

set -euo pipefail

DIR="$(cd "$(dirname "$0")/.." && pwd)"
RESULTS="$DIR/results"
mkdir -p "$RESULTS"

DB="postgresql://recruitment:recruitment123@localhost:5432/recruitment_dw"

run_query() {
  local name="$1"
  local query="$2"
  echo "[EXPORT] $name"
  psql "$DB" -A -F "," -c "$query" > "$RESULTS/${name}.csv"
}

run_query "R1_hiring_trends" "
SELECT d.year, d.month_name,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
"

run_query "R2_technology_analysis" "
SELECT t.technology_name,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hired DESC;
"

run_query "R3_candidate_profile" "
SELECT c.seniority,
       CASE
           WHEN c.yoe < 5  THEN '0-4 years'
           WHEN c.yoe < 10 THEN '5-9 years'
           WHEN c.yoe < 20 THEN '10-19 years'
           ELSE '20+ years'
       END AS experience_range,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.seniority, experience_range
ORDER BY c.seniority, experience_range;
"

run_query "R4_geographic_analysis" "
SELECT c.country,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.country
ORDER BY total_applications DESC
LIMIT 20;
"

run_query "R5_assessment_analysis" "
SELECT a.code_challenge_score,
       a.technical_interview_score,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired
FROM fact_applications f
JOIN dim_assessment a ON f.assessment_key = a.assessment_key
GROUP BY a.code_challenge_score, a.technical_interview_score
ORDER BY a.code_challenge_score, a.technical_interview_score;
"

echo ""
echo "[EXPORT] Done. Files saved in $RESULTS/"
ls -la "$RESULTS/"
