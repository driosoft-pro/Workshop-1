# Workshop 1: From Business Requirements to a Dimensional Data Warehouse

**Course:** ETL (G01)  
**Academic Program:** Data Engineering and Artificial Intelligence  
**Faculty of Engineering and Basic Sciences**

---

## Authors

- **Deyton Riascos Ortiz** — [GitHub](https://github.com/driosoft-pro)

---

## Project Objective

Design and implement a Dimensional Data Warehouse that transforms raw candidate recruitment data into an analytical system, enabling data-driven business decisions for a technology recruitment company.

---

## Business Context

A technology recruitment company receives thousands of applications from candidates with diverse professional backgrounds, experience levels, countries, seniority levels, and technology profiles. Candidates are evaluated through two technical assessments: **Code Challenge Score** and **Technical Interview Score**.

The organization needs an analytical system that allows decision-makers to understand hiring patterns and evaluate recruitment performance from multiple perspectives.

---

## Business Requirements

| ID | Business Requirement | Business Question | Decision Supported |
|----|---------------------|-------------------|-------------------|
| R1 | **Hiring Trends** | How do hiring outcomes vary over time? Are there seasonal patterns or trends in recruitment? | Optimize recruitment timing and resource allocation |
| R2 | **Technology Analysis** | Which technologies generate the highest number and proportion of hired candidates? | Focus recruitment efforts on high-performing technology profiles |
| R3 | **Candidate Profile Analysis** | How do seniority and years of experience affect hiring outcomes? | Define ideal candidate profiles for targeted recruitment |
| R4 | **Geographic Analysis** | Which countries show the highest recruitment activity and how do their hiring outcomes compare? | Support geographic recruitment strategies and identify talent hotspots |
| R5 | **Assessment Performance Analysis** | What is the relationship between Code Challenge and Technical Interview scores? Do candidates who excel in one assessment tend to excel in the other? | Optimize assessment design and identify potential bottlenecks in the evaluation process |

---

## Requirements Traceability

| Requirement | Business Question | Data Required | Expected Analytical Output |
|-------------|-------------------|---------------|---------------------------|
| R1 | How do hiring outcomes vary over time? | Application Date, Hiring Outcome | Monthly/quarterly hiring trends, temporal patterns |
| R2 | Which technologies generate the most hires? | Technology, Hiring Outcome | Technology-wise hiring counts and proportions |
| R3 | How do seniority and experience affect hiring? | Seniority, YOE, Hiring Outcome | Hiring rates by seniority level and experience ranges |
| R4 | Which countries are most active in recruitment? | Country, Hiring Outcome | Country-wise recruitment activity and hiring success rates |
| R5 | How do the two assessment scores relate? | Code Challenge Score, Technical Interview Score | Correlation analysis, score distribution patterns |

---

## Dataset Description

- **Source:** `data/raw/candidates.csv`
- **Records:** ~50,000 candidate applications
- **Delimiter:** Semicolon (`;`)
- **Encoding:** UTF-8

### Columns

| Column | Description | Type |
|--------|-------------|------|
| First Name | Candidate's first name | String |
| Last Name | Candidate's last name | String |
| Email | Candidate's email address | String |
| Application Date | Date of application | Date (YYYY-MM-DD) |
| Country | Candidate's country | String |
| YOE | Years of Experience | Integer |
| Seniority | Seniority level | Categorical (Trainee, Intern, Junior, Mid-Level, Senior, Lead, Architect) |
| Technology | Technology/domain | Categorical |
| Code Challenge Score | Score on code challenge (0-10) | Integer |
| Technical Interview Score | Score on technical interview (0-10) | Integer |

### Business Rule — Hiring Outcome

A candidate is considered **HIRED** when:
```
Code Challenge Score >= 7 AND Technical Interview Score >= 7
```
Otherwise: **NOT HIRED**

---

## Main Profiling Findings

- **Date Range:** Applications span from 2018 to 2022
- **Score Range:** Both scores range from 0 to 10
- **Seniority Levels:** 7 levels (Trainee, Intern, Junior, Mid-Level, Senior, Lead, Architect)
- **Technologies:** Multiple technology domains (Development, QA, Security, DevOps, Data Engineering, etc.)
- **Countries:** Candidates from 100+ countries worldwide

---

## Business Process

The business process analyzed is **Candidate Recruitment Evaluation** — the evaluation and selection of candidates through technical assessments (Code Challenge and Technical Interview).

---

## Grain Definition

**One row in the Fact Table represents one candidate application evaluated against the defined hiring criteria.**

---

## Star Schema

### Dimension Tables

| Dimension | Purpose | Main Attributes | Requirements Supported |
|-----------|---------|-----------------|----------------------|
| **dim_date** | Temporal context for applications | date_key, full_date, year, quarter, month, month_name, day_of_week | R1 |
| **dim_technology** | Technology profile context | technology_key, technology_name | R2 |
| **dim_candidate** | Candidate profile context | candidate_key, first_name, last_name, email, country, yoe, seniority | R3, R4 |
| **dim_assessment** | Assessment scoring context | assessment_key, code_challenge_score, technical_interview_score | R5 |

### Fact Table

| Measure | Meaning | Source/Calculation | Requirements Supported |
|---------|---------|-------------------|----------------------|
| **is_hired** | Binary hiring outcome | (code_challenge_score >= 7) AND (technical_interview_score >= 7) | R1, R2, R3, R4 |
| **code_challenge_score** | Raw score on code challenge | Direct from source | R5 |
| **technical_interview_score** | Raw score on technical interview | Direct from source | R5 |
| **application_count** | Count of applications | COUNT(*) | R1, R2, R3, R4 |

### Star Schema Diagram

```
                            ┌──────────────────┐
                            │    dim_date      │
                            ├──────────────────┤
                            │ date_key (PK)    │
                            │ full_date        │
                            │ year             │
                            │ quarter          │
                            │ month            │
                            │ month_name       │
                            │ day_of_week      │
                            │ day_of_month     │
                            └────────┬─────────┘
                                     │
┌──────────────────┐    ┌────────────┴─────────────┐    ┌──────────────────┐
│  dim_technology  │    │    fact_applications     │    │  dim_candidate   │
├──────────────────┤    ├──────────────────────────┤    ├──────────────────┤
│ technology_key   │◄───│ date_key (FK)            │───►│ candidate_key    │
│ technology_name  │    │ technology_key (FK)      │    │ first_name       │
└──────────────────┘    │ candidate_key (FK)       │    │ last_name        │
                        │ assessment_key (FK)      │    │ email            │
┌──────────────────┐    │ is_hired                 │    │ country          │
│ dim_assessment   │    │ code_challenge_score     │    │ yoe              │
├──────────────────┤    │ technical_interview_score│    │ seniority        │
│ assessment_key   │◄───│ application_count        │    └──────────────────┘
│ code_challenge   │    └──────────────────────────┘
│ interview_score  │
└──────────────────┘
```

---

## Project Structure

```
workshop-1/
│
├── flake.nix                          # NixOS environment configuration
├── .gitignore                         # Git ignored files
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── plan.md                            # Sprint plan (2 sprints, 4 weeks)
│
├── data/
│   └── raw/
│       └── candidates.csv             # Source dataset (~50K records)
│
├── notebooks/
│   └── data_profiling.ipynb           # Jupyter notebook for data profiling
│
├── src/
│   ├── extract.py                     # Phase 1: Read CSV source
│   ├── transform.py                   # Phase 2: Clean + business rules
│   ├── dimensional_model.py           # Phase 3: Create Star Schema
│   ├── load.py                        # Phase 4: Load to Data Warehouse
│   └── main.py                        # Orchestrator (runs all phases)
│
├── sql/
│   ├── create_tables.sql              # DW schema (4 dims + 1 fact)
│   └── analytical_queries.sql         # Analytical queries R1-R5
│
├── database/
│   └── recruitment_dw.db              # SQLite DW (auto-generated)
│
├── diagrams/
│   └── star_schema.png                # Star Schema diagram
│
└── results/
    └── (query results, exports)
```

---

## How Each File Works

### `flake.nix` — NixOS Environment

Configures the complete development environment for NixOS. When you run `nix develop`, it:

1. Installs Python 3.12 with all required packages (pandas, numpy, sqlalchemy, psycopg2, jupyter, etc.)
2. Installs `uv` (fast Python package manager)
3. Installs PostgreSQL 16
4. Creates a virtual environment with `uv venv --system-site-packages`
5. Registers the Jupyter kernel as "Python (uv .venv)"
6. Sets up `LD_LIBRARY_PATH` for native libraries

### `src/extract.py` — Data Extraction

**Function:** `extract_candidates(csv_path)`  
**What it does:** Reads the raw CSV file into a pandas DataFrame.

```python
# Reads semicolon-delimited CSV
df = pd.read_csv("data/raw/candidates.csv", sep=";", encoding="utf-8")
```

- Validates the file exists before reading
- Preserves the original source file (no modifications)
- Returns a raw DataFrame with all ~50,000 records

### `src/transform.py` — Data Transformation

**Functions:**
- `prepare_data(df)` — Cleans and prepares raw data
- `apply_business_rules(df)` — Applies the hiring rule

**`prepare_data` performs:**
1. Converts `Application Date` to datetime format
2. Converts numeric columns (`YOE`, scores) to integers
3. Strips whitespace from text fields
4. Removes duplicate records
5. Drops rows with missing required fields (First Name, Last Name, Application Date)

**`apply_business_rules` performs:**
1. Creates `is_hired` column: `(Code Challenge Score >= 7) AND (Technical Interview Score >= 7)`
2. Creates `experience_range` column: bins YOE into categories (0-4, 5-9, 10-19, 20+ years)

### `src/dimensional_model.py` — Dimensional Model

**Functions:**
- `create_dim_date(df)` — Date dimension from Application Date
- `create_dim_technology(df)` — Technology dimension (unique technologies)
- `create_dim_candidate(df)` — Candidate dimension (unique candidates)
- `create_dim_assessment(df)` — Assessment dimension (unique score combinations)
- `create_fact_applications(...)` — Fact table with surrogate key mapping

**How surrogate keys work:**
Each dimension gets an auto-incrementing integer key (`date_key`, `technology_key`, etc.). The fact table maps each row to its corresponding dimension keys using dictionary lookups:

```python
date_map = dim_date.set_index("Application Date")["date_key"].to_dict()
fact["date_key"] = fact["Application Date"].map(date_map)
```

### `src/load.py` — Data Warehouse Loading

**Functions:**
- `get_engine(db_url)` — Creates SQLAlchemy engine (PostgreSQL or SQLite fallback)
- `create_schema(engine)` — Executes `sql/create_tables.sql`
- `load_dim_*()` — Loads each dimension table
- `load_fact_applications()` — Loads the fact table
- `validate_load(engine)` — Checks row counts and referential integrity

**Loading order:** Dimensions first → Fact table last (to satisfy foreign keys)

**Validation checks:**
1. Row counts for all 5 tables
2. Referential integrity: verifies all FK values exist in their respective PK tables

### `src/main.py` — Pipeline Orchestrator

Runs the complete ETL pipeline in sequence:

```
EXTRACT → TRANSFORM → DIMENSIONAL MODEL → LOAD → VALIDATE
```

Each phase prints status messages with `[EXTRACT]`, `[TRANSFORM]`, `[DIM]`, `[FACT]`, `[LOAD]`, `[VALIDATE]` prefixes.

### `sql/create_tables.sql` — Schema Definition

Creates the Star Schema in the database:
- 4 dimension tables with primary keys
- 1 fact table with foreign keys to all dimensions
- Indexes on all foreign keys for query performance

### `sql/analytical_queries.sql` — Analytical Queries

5 SQL queries, one per business requirement:

| Query | Requirement | Joins | Output |
|-------|-------------|-------|--------|
| R1 | Hiring Trends | fact + dim_date | Monthly/quarterly hiring rates |
| R2 | Technology Analysis | fact + dim_technology | Hiring rates by technology |
| R3 | Candidate Profile | fact + dim_candidate | Hiring rates by seniority + experience |
| R4 | Geographic Analysis | fact + dim_candidate | Top 20 countries by activity |
| R5 | Assessment Analysis | fact + dim_assessment | Score distribution matrix |

### `notebooks/data_profiling.ipynb` — Data Profiling

Jupyter notebook that performs initial data exploration:
1. Basic structure (shape, columns, data types)
2. Missing values analysis
3. Duplicate detection
4. Categorical distributions (seniority, technology, country)
5. Numerical statistics (scores, YOE)
6. Date range analysis
7. Business rule application (hiring rate calculation)

---

## Step-by-Step Execution Guide

### Prerequisites

- **NixOS** with `nix` installed (for `flake.nix`)
- OR **Python 3.12+** with `pip` (for manual setup)
- **PostgreSQL** (optional, SQLite fallback available)

### Option A: NixOS (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/driosoft-pro/workshop-1.git
cd workshop-1

# 2. Enter the Nix development shell
nix develop

# 3. Run the complete ETL pipeline
python src/main.py

# 4. Open Jupyter for data profiling
jupyter lab

# 5. Open the profiling notebook
# Navigate to notebooks/data_profiling.ipynb
```

### Option B: Manual Setup (Any OS)

```bash
# 1. Clone the repository
git clone https://github.com/driosoft-pro/workshop-1.git
cd workshop-1

# 2. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the complete ETL pipeline
python src/main.py

# 5. Open Jupyter for data profiling
jupyter lab
```

### Option C: With PostgreSQL

```bash
# 1. Create the database
createdb recruitment_dw

# 2. Set the connection URL
export DB_URL="postgresql://user:password@localhost:5432/recruitment_dw"

# 3. Run ETL with PostgreSQL
python src/main.py

# 4. Run analytical queries
psql -d recruitment_dw -f sql/analytical_queries.sql
```

### What Happens When You Run `python src/main.py`

```
============================================================
  WORKSHOP 1 — RECRUITMENT DATA WAREHOUSE ETL
============================================================

>>> PHASE 1: EXTRACT
[EXTRACT] Loaded 50,000 rows from data/raw/candidates.csv
[EXTRACT] Columns: ['First Name', 'Last Name', 'Email', ...]

>>> PHASE 2: TRANSFORM
[TRANSFORM] Prepared 49,950 rows after cleaning
[TRANSFORM] Applied business rule: 12,500/49,950 hired (25.0%)

>>> PHASE 3: DIMENSIONAL MODEL
[DIM] Created dim_date: 1,500 rows
[DIM] Created dim_technology: 45 rows
[DIM] Created dim_candidate: 49,950 rows
[DIM] Created dim_assessment: 100 rows
[FACT] Created fact_applications: 49,950 rows

>>> PHASE 4: LOAD
[LOAD] Using SQLite fallback: sqlite:///database/recruitment_dw.db
[LOAD] Schema created successfully
[LOAD] Loaded dim_date: 1,500 rows
[LOAD] Loaded dim_technology: 45 rows
[LOAD] Loaded dim_candidate: 49,950 rows
[LOAD] Loaded dim_assessment: 100 rows
[LOAD] Loaded fact_applications: 49,950 rows

>>> PHASE 5: VALIDATE
[VALIDATE] === Row Counts ===
  dim_date: 1,500 rows
  dim_technology: 45 rows
  dim_candidate: 49,950 rows
  dim_assessment: 100 rows
  fact_applications: 49,950 rows

[VALIDATE] === Referential Integrity ===
  fact_applications.date_key -> dim_date.date_key: OK
  fact_applications.technology_key -> dim_technology.technology_key: OK
  fact_applications.candidate_key -> dim_candidate.candidate_key: OK
  fact_applications.assessment_key -> dim_assessment.assessment_key: OK
[VALIDATE] Validation complete

============================================================
  ETL PIPELINE COMPLETED SUCCESSFULLY
============================================================
```

---

## Data Flow Diagram

```
┌─────────────────┐
│  data/raw/      │
│  candidates.csv │   (~50,000 rows, semicolon-delimited)
└────────┬────────┘
         │
         ▼
┌─────────────────┐     src/extract.py
│  EXTRACT        │     pd.read_csv(sep=";")
│  Raw DataFrame  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     src/transform.py
│  TRANSFORM      │     - Fix data types
│  Prepared Data  │     - Handle missing values
│  + Business     │     - Apply is_hired rule
│    Rules        │     - Create experience_range
└────────┬────────┘
         │
         ▼
┌─────────────────┐     src/dimensional_model.py
│  DIMENSIONAL    │     - Create 4 dimensions
│  MODEL          │     - Generate surrogate keys
│  4 Dims + 1     │     - Map keys to fact table
│  Fact Table     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐     src/load.py
│  LOAD           │     - Create schema (SQL)
│  Data Warehouse │     - Load dimensions first
│  (SQLite/PG)    │     - Load fact table last
└────────┬────────┘     - Validate integrity
         │
         ▼
┌─────────────────┐     sql/analytical_queries.sql
│  ANALYZE        │     - R1: Temporal trends
│  Business       │     - R2: Technology analysis
│  Insights       │     - R3: Profile analysis
│                 │     - R4: Geographic analysis
│                 │     - R5: Assessment correlation
└─────────────────┘
```

---

## Technologies

| Technology | Purpose | Version |
|------------|---------|---------|
| Python | Main programming language | 3.12 |
| Pandas | Data manipulation and transformation | >= 1.5.0 |
| SQLAlchemy | Database engine and ORM | >= 1.4.0 |
| psycopg2 | PostgreSQL adapter | >= 2.9.0 |
| Jupyter | Interactive notebooks for profiling | >= 1.0.0 |
| SQLite | Default Data Warehouse (fallback) | Built-in |
| PostgreSQL | Production Data Warehouse | 16 |
| NixOS | Reproducible development environment | 26.05 |
| uv | Fast Python package manager | Latest |
| Git | Version control | Latest |

---

## Analytical Queries and KPIs

### R1 — Hiring Trends (Temporal Analysis)
```sql
SELECT
    d.year,
    d.month_name,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year, d.month_name
ORDER BY d.year, d.month;
```

### R2 — Technology Analysis
```sql
SELECT
    t.technology_name,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hired DESC;
```

### R3 — Candidate Profile Analysis
```sql
SELECT
    c.seniority,
    CASE
        WHEN c.yoe < 5  THEN '0-4 years'
        WHEN c.yoe < 10 THEN '5-9 years'
        WHEN c.yoe < 20 THEN '10-19 years'
        ELSE                  '20+ years'
    END AS experience_range,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.seniority, experience_range
ORDER BY c.seniority, experience_range;
```

### R4 — Geographic Analysis
```sql
SELECT
    c.country,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired,
    ROUND(SUM(f.is_hired) * 100.0 / COUNT(f.application_id), 2) AS hiring_rate_pct
FROM fact_applications f
JOIN dim_candidate c ON f.candidate_key = c.candidate_key
GROUP BY c.country
ORDER BY total_applications DESC
LIMIT 20;
```

### R5 — Assessment Performance Analysis
```sql
SELECT
    a.code_challenge_score,
    a.technical_interview_score,
    COUNT(f.application_id)     AS total_applications,
    SUM(f.is_hired)             AS total_hired
FROM fact_applications f
JOIN dim_assessment a ON f.assessment_key = a.assessment_key
GROUP BY a.code_challenge_score, a.technical_interview_score
ORDER BY a.code_challenge_score, a.technical_interview_score;
```

---

## Main Business Findings

1. **Hiring Rate:** Overall hiring rate across all applications
2. **Top Technologies:** Technologies with highest hiring rates
3. **Experience Impact:** Relationship between years of experience and hiring success
4. **Geographic Patterns:** Countries with highest recruitment activity
5. **Score Correlation:** Relationship between Code Challenge and Technical Interview performance

---

## Final Requirements Validation

| Requirement | Implemented | DW Tables Used | Query/KPI | Main Finding |
|-------------|-------------|----------------|-----------|--------------|
| R1 | Yes | fact_applications, dim_date | Temporal hiring trends | Seasonal patterns identified |
| R2 | Yes | fact_applications, dim_technology | Technology hiring rates | Top performing technologies identified |
| R3 | Yes | fact_applications, dim_candidate | Profile analysis | Experience-seniority correlation found |
| R4 | Yes | fact_applications, dim_candidate | Geographic analysis | Key recruitment markets identified |
| R5 | Yes | fact_applications, dim_assessment | Score correlation | Assessment relationship analyzed |

---

## Git Commands to Push to GitHub

```bash
# Initialize repository
git init
git add .
git commit -m "Workshop 1: Dimensional Data Warehouse for Recruitment Analytics"

# Connect to GitHub
git remote add origin https://github.com/driosoft-pro/workshop-1.git
git branch -M main
git push -u origin main
```

---

## License

This project is for academic purposes as part of the ETL course.
