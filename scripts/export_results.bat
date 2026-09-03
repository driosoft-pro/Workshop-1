@echo off
REM export_results.bat — Export analytical query results to CSV (Windows)

setlocal enabledelayedexpansion

REM Find project root (parent of scripts/)
set "SCRIPT_DIR=%~dp0"
set "PROJECT_DIR=%SCRIPT_DIR%.."
set "RESULTS=%PROJECT_DIR%\results"
if not exist "%RESULTS%" mkdir "%RESULTS%"

set "DB=postgresql://recruitment:recruitment123@localhost:5432/recruitment_dw"

echo [EXPORT] R1_hiring_trends
psql "%DB%" -A -F "," -c "SELECT d.year, d.month_name, COUNT(f.application_id) AS total_applications, SUM(f.is_hired) AS total_hired, ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct FROM fact_applications f JOIN dim_date d ON f.date_key = d.date_key GROUP BY d.year, d.month, d.month_name ORDER BY d.year, d.month;" > "%RESULTS%\R1_hiring_trends.csv"

echo [EXPORT] R2_technology_analysis
psql "%DB%" -A -F "," -c "SELECT t.technology_name, COUNT(f.application_id) AS total_applications, SUM(f.is_hired) AS total_hired, ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct FROM fact_applications f JOIN dim_technology t ON f.technology_key = t.technology_key GROUP BY t.technology_name ORDER BY total_hired DESC;" > "%RESULTS%\R2_technology_analysis.csv"

echo [EXPORT] R3_candidate_profile
psql "%DB%" -A -F "," -c "SELECT c.seniority, CASE WHEN c.yoe ^< 5 THEN '0-4 years' WHEN c.yoe ^< 10 THEN '5-9 years' WHEN c.yoe ^< 20 THEN '10-19 years' ELSE '20+ years' END AS experience_range, COUNT(f.application_id) AS total_applications, SUM(f.is_hired) AS total_hired, ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct FROM fact_applications f JOIN dim_candidate c ON f.candidate_key = c.candidate_key GROUP BY c.seniority, experience_range ORDER BY c.seniority, experience_range;" > "%RESULTS%\R3_candidate_profile.csv"

echo [EXPORT] R4_geographic_analysis
psql "%DB%" -A -F "," -c "SELECT c.country, COUNT(f.application_id) AS total_applications, SUM(f.is_hired) AS total_hired, ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct FROM fact_applications f JOIN dim_candidate c ON f.candidate_key = c.candidate_key GROUP BY c.country ORDER BY total_applications DESC LIMIT 20;" > "%RESULTS%\R4_geographic_analysis.csv"

echo [EXPORT] R5_assessment_analysis
psql "%DB%" -A -F "," -c "SELECT a.code_challenge_score, a.technical_interview_score, COUNT(f.application_id) AS total_applications, SUM(f.is_hired) AS total_hired FROM fact_applications f JOIN dim_assessment a ON f.assessment_key = a.assessment_key GROUP BY a.code_challenge_score, a.technical_interview_score ORDER BY a.code_challenge_score, a.technical_interview_score;" > "%RESULTS%\R5_assessment_analysis.csv"

echo.
echo [EXPORT] Done. Files saved in %RESULTS%
dir "%RESULTS%\R*.csv"

endlocal
