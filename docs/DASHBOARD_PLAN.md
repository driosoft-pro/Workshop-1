# Dashboard Plan: Recruitment Analytics

**File:** `dashboard_recruitment.pbix`
**Tool:** Power BI Desktop (or pbix-mcp for programmatic generation)
**Data Source:** PostgreSQL `recruitment_dw` (DirectQuery)

---

## Pages Overview

| Page | Title | Requirement | Purpose |
|------|-------|-------------|---------|
| 1 | Overview | General | Executive summary of recruitment metrics |
| 2 | Hiring Trends | R1 | Temporal analysis of hiring outcomes |
| 3 | Technology Analysis | R2 | Hiring rates by technology domain |
| 4 | Candidate Profile | R3 | Impact of seniority and experience |
| 5 | Geographic Analysis | R4 | Top countries by recruitment activity |
| 6 | Assessment Analysis | R5 | Relationship between Code Challenge and Technical Interview scores |

---

## Page 1: Overview

### KPI Cards

| Card | DAX Measure |
|------|-------------|
| Total Applications | `COUNT(fact_applications[application_id])` |
| Total Hired | `SUM(fact_applications[is_hired])` |
| Hiring Rate % | `DIVIDE(SUM(fact_applications[is_hired]), COUNT(fact_applications[application_id])) * 100` |

### Visuals

| Visual | Type | X-Axis | Y-Axis | Legend |
|--------|------|--------|--------|-------|
| Applications by Technology | Donut Chart | — | `COUNT(*)` | `dim_technology[technology_name]` |
| Applications by Year | Clustered Bar | `dim_date[year]` | `COUNT(*)` | — |
| Applications by Seniority | Clustered Column | `dim_candidate[seniority]` | `COUNT(*)` | — |

---

## Page 2: R1 — Hiring Trends

### Data Source

Query: `fact_applications` JOIN `dim_date`

```sql
SELECT d.year, d.month_name, d.month,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

### Visuals

| Visual | Type | X-Axis | Y-Axis | Legend |
|--------|------|--------|--------|-------|
| Monthly Hiring Rate Trend | Line Chart | `dim_date[year]` + `dim_date[month_name]` | `hiring_rate_pct` | — |
| Applications vs Hired | Clustered Column | `dim_date[month_name]` | `total_applications`, `total_hired` | — |
| Quarterly Summary | Matrix | `dim_date[year]` (rows) | `dim_date[quarter]` (columns) | `hiring_rate_pct` (values) |

### Key Metrics

- Monthly hiring rate ranges from ~11% to ~17%
- Peak hiring: July 2022 (16.96%)
- Lowest hiring: April 2018 (11.49%)

---

## Page 3: R2 — Technology Analysis

### Data Source

Query: `fact_applications` JOIN `dim_technology`

```sql
SELECT t.technology_name,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hired DESC;
```

### Visuals

| Visual | Type | X-Axis | Y-Axis | Legend |
|--------|------|--------|--------|-------|
| Top Technologies by Hired | Horizontal Bar | `total_hired` | `dim_technology[technology_name]` | — |
| Hiring Rate by Technology | Treemap | — | `hiring_rate_pct` | `dim_technology[technology_name]` |
| Technology Details | Table | — | `technology_name`, `total_applications`, `total_hired`, `hiring_rate_pct` | — |

### Key Metrics

- Top 3: Game Development (519), DevOps (495), System Administration (293)
- Highest hiring rate: Development - CMS Backend (15.09%)
- Lowest hiring rate: Technical Writing (11.73%)

---

## Page 4: R3 — Candidate Profile

### Data Source

Query: `fact_applications` JOIN `dim_candidate`

```sql
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
```

### Visuals

| Visual | Type | X-Axis | Y-Axis | Legend |
|--------|------|--------|--------|-------|
| Hiring Rate by Seniority | Clustered Bar | `hiring_rate_pct` | `dim_candidate[seniority]` | — |
| Experience Range vs Hired | Stacked Column | `experience_range` | `total_hired` | `dim_candidate[seniority]` |
| Profile Matrix | Matrix | `seniority` (rows) | `experience_range` (columns) | `hiring_rate_pct` (values) |

### Key Metrics

- Highest hiring rate: Intern + 0-4 years (16.27%)
- Seniority levels: Trainee, Intern, Junior, Mid-Level, Senior, Lead, Architect
- Experience ranges: 0-4, 5-9, 10-19, 20+ years

---

## Page 5: R4 — Geographic Analysis

### Data Source

Query: `fact_applications` JOIN `dim_candidate`

```sql
SELECT c.country,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired,
       ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.country
ORDER BY total_applications DESC
LIMIT 20;
```

### Visuals

| Visual | Type | Location | Size | Color |
|--------|------|----------|------|-------|
| World Map | Map | `dim_candidate[country]` | `total_applications` | `hiring_rate_pct` |
| Top 20 Countries | Horizontal Bar | `total_applications` | `dim_candidate[country]` | — |
| Country Details | Table | — | `country`, `total_applications`, `total_hired`, `hiring_rate_pct` | — |

### Key Metrics

- Top country by applications: Malawi (242)
- Highest hiring rate: Niger (17.32%)
- Lowest hiring rate: Malawi (9.50%)

---

## Page 6: R5 — Assessment Analysis

### Data Source

Query: `fact_applications` JOIN `dim_assessment`

```sql
SELECT a.code_challenge_score,
       a.technical_interview_score,
       COUNT(f.application_id) AS total_applications,
       SUM(f.is_hired) AS total_hired
FROM fact_applications f
JOIN dim_assessment a ON f.assessment_key = a.assessment_key
GROUP BY a.code_challenge_score, a.technical_interview_score
ORDER BY a.code_challenge_score, a.technical_interview_score;
```

### Visuals

| Visual | Type | Rows | Columns | Values |
|--------|------|------|---------|--------|
| Score Matrix | Matrix | `code_challenge_score` | `technical_interview_score` | `total_applications` |
| Hired Heatmap | Matrix | `code_challenge_score` | `technical_interview_score` | `total_hired` |
| Score Distribution | Clustered Column | `code_challenge_score` | `total_applications` | — |

### Key Metrics

- Hire threshold: BOTH scores >= 7
- Total hired: 6,698 (13.4%)
- Score range: 0-10 for both assessments

---

## DAX Measures (Global)

```dax
Total Applications = COUNT(fact_applications[application_id])

Total Hired = SUM(fact_applications[is_hired])

Hiring Rate = DIVIDE([Total Hired], [Total Applications]) * 100

Avg Code Challenge Score = AVERAGE(fact_applications[code_challenge_score])

Avg Interview Score = AVERAGE(fact_applications[technical_interview_score])
```

---

## Relationships

```
fact_applications[date_key]       → dim_date[date_key]
fact_applications[technology_key] → dim_technology[technology_key]
fact_applications[candidate_key]  → dim_candidate[candidate_key]
fact_applications[assessment_key] → dim_assessment[assessment_key]
```

---

## Connection Settings (PostgreSQL)

| Setting | Value |
|---------|-------|
| Server | `localhost:5432` |
| Database | `recruitment_dw` |
| Username | `recruitment` |
| Password | `recruitment123` |
| Data Connectivity | Import (recommended) or DirectQuery |
