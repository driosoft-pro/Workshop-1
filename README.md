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

### Dimension Details

#### dim_date — Temporal Dimension

**Why it exists:** Recruitment patterns are highly seasonal. Understanding when candidates apply and when hiring decisions are made is critical for resource planning and optimizing recruitment timing.

**Business requirement:** R1 — Hiring Trends

**Attributes:**
- `date_key` — Surrogate key for joining with the fact table
- `full_date` — Complete date in YYYY-MM-DD format
- `year`, `quarter`, `month` — Numeric temporal components for aggregation
- `month_name` — Human-readable month name for reports
- `day_of_week` — Day of the week (e.g., Monday, Tuesday)

**How it is used:**
- Group applications by month/quarter/year to identify seasonal hiring patterns
- Compare hiring rates across different time periods
- Detect trends in recruitment activity over the years (2018–2022)
- Example query: "Which months have the highest hiring rate?"

#### dim_technology — Technology Dimension

**Why it exists:** The company recruits for multiple technology roles (Development, QA, Security, DevOps, etc.). Understanding which technologies have the best hiring outcomes helps focus recruitment efforts on high-performing profiles.

**Business requirement:** R2 — Technology Analysis

**Attributes:**
- `technology_key` — Surrogate key
- `technology_name` — Technology domain name (e.g., "Development - Backend", "QA Automation", "Security")

**How it is used:**
- Compare hiring rates across different technology domains
- Identify which technologies produce the most hired candidates
- Allocate recruitment resources to high-performing technology areas
- Example query: "Which technology has the highest proportion of hired candidates?"

#### dim_candidate — Candidate Profile Dimension

**Why it exists:** Candidate attributes such as seniority, years of experience, and geographic location directly impact hiring outcomes. This dimension enables profiling candidates to define ideal recruitment targets.

**Business requirements:** R3 — Candidate Profile Analysis, R4 — Geographic Analysis

**Attributes:**
- `candidate_key` — Surrogate key
- `first_name`, `last_name`, `email` — Candidate identification
- `country` — Country of origin
- `yoe` — Years of experience (numeric)
- `seniority` — Seniority level (Trainee, Intern, Junior, Mid-Level, Senior, Lead, Architect)

**How it is used:**
- Analyze hiring rates by seniority level to identify which levels get hired most often
- Segment candidates by years of experience (0–4, 5–9, 10–19, 20+) and compare outcomes
- Identify top countries by recruitment activity and hiring success
- Define ideal candidate profiles for targeted recruitment campaigns
- Example queries: "Do Senior candidates have higher hiring rates than Juniors?" and "Which countries generate the most hires?"

#### dim_assessment — Assessment Dimension

**Why it exists:** Candidates are evaluated through two technical assessments: Code Challenge and Technical Interview. Understanding the relationship between these scores helps optimize the assessment design and identify bottlenecks in the evaluation process.

**Business requirement:** R5 — Assessment Performance Analysis

**Attributes:**
- `assessment_key` — Surrogate key
- `code_challenge_score` — Score on the code challenge (0–10)
- `technical_interview_score` — Score on the technical interview (0–10)

**How it is used:**
- Analyze the distribution of score combinations across all applications
- Identify whether candidates who excel in one assessment also excel in the other
- Detect if one assessment is a bottleneck (e.g., many candidates fail the code challenge but pass the interview)
- Validate the hiring threshold (both scores >= 7) against actual outcomes
- Example query: "What is the correlation between Code Challenge and Technical Interview scores?"

### Fact Table

| Measure | Meaning | Source/Calculation | Requirements Supported |
|---------|---------|-------------------|----------------------|
| **is_hired** | Binary hiring outcome | (code_challenge_score >= 7) AND (technical_interview_score >= 7) | R1, R2, R3, R4 |
| **code_challenge_score** | Raw score on code challenge | Direct from source | R5 |
| **technical_interview_score** | Raw score on technical interview | Direct from source | R5 |
| **application_count** | Count of applications | COUNT(*) | R1, R2, R3, R4 |

### Star Schema Diagram

![Star Schema](diagrams/star_schema.png)

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
├── .env.example                       # Environment variables template
├── docker-compose.yml                 # PostgreSQL Docker/Podman setup
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
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
├── scripts/
│   ├── export_results.sh              # Export analytical queries to CSV (Linux/macOS)
│   ├── export_results.bat             # Export analytical queries to CSV (Windows)
│   └── generate_dashboard.py          # Generate Power BI dashboard (.pbix)
│
├── dashboard_recruitment.pbix         # Power BI dashboard (6 pages, R1-R5)
│
├── sql/
│   ├── create_tables.sql              # DW schema (4 dims + 1 fact)
│   └── analytical_queries.sql         # Analytical queries R1-R5
│
├── database/                          # PostgreSQL data (gitignored)
│
├── diagrams/
│   └── star_schema.png                # Star Schema diagram
│
├── results/                           # Query results (CSV exports)
│   ├── R1_hiring_trends.csv
│   ├── R2_technology_analysis.csv
│   ├── R3_candidate_profile.csv
│   ├── R4_geographic_analysis.csv
│   └── R5_assessment_analysis.csv
│
├── docs/
│   ├── DASHBOARD_PLAN.md              # Dashboard design plan
│   └── ETL_2026-2_Workshop-1.pdf      # Workshop specification
│
└── docs/
    └── ETL_2026-2_Workshop-1.pdf      # Workshop specification
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
- `get_engine(db_url)` — Creates SQLAlchemy engine for PostgreSQL
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

### `scripts/export_results.sh` / `scripts/export_results.bat` — Results Exporter

Executes all 5 analytical queries and exports results to CSV files in `results/`.

**Linux/macOS:**
```bash
scripts/export_results.sh
```

**Windows:**
```cmd
scripts\export_results.bat
```

Requires `psql` to be available (automatically available inside `nix develop` on Linux, or install PostgreSQL on Windows). Each query result is saved as a separate CSV file: `R1_hiring_trends.csv` through `R5_assessment_analysis.csv`.

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

### Quick Start (Podman)

```bash
# 1. Start PostgreSQL database
podman-compose up -d

# If podman-compose is not installed, use:
podman run -d \
  --name recruitment_dw_postgres \
  -e POSTGRES_DB=recruitment_dw \
  -e POSTGRES_USER=recruitment \
  -e POSTGRES_PASSWORD=recruitment123 \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  --restart unless-stopped \
  postgres:16-alpine

# 2. Wait for database to be ready
podman exec recruitment_dw_postgres pg_isready -U recruitment

# 3. Export database URL
export DB_URL="postgresql://recruitment:recruitment123@localhost:5432/recruitment_dw"

# 4. Run the ETL pipeline
python src/main.py
```

### Full Setup from Scratch

```bash
# 1. Clone the repository
git clone https://github.com/driosoft-pro/workshop-1.git
cd workshop-1

# 2. Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Start PostgreSQL with Podman
podman-compose up -d
# OR without podman-compose:
podman run -d \
  --name recruitment_dw_postgres \
  -e POSTGRES_DB=recruitment_dw \
  -e POSTGRES_USER=recruitment \
  -e POSTGRES_PASSWORD=recruitment123 \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  --restart unless-stopped \
  postgres:16-alpine

# 4. Wait for database to be ready
podman exec recruitment_dw_postgres pg_isready -U recruitment

# 5. Export database URL
export DB_URL="postgresql://recruitment:recruitment123@localhost:5432/recruitment_dw"

# 6. Run the ETL pipeline
python src/main.py

# 7. Run analytical queries
psql -h localhost -U recruitment -d recruitment_dw -f sql/analytical_queries.sql

# 8. Open Jupyter for data profiling
jupyter lab
```

### NixOS Setup

```bash
# 1. Clone the repository
git clone https://github.com/driosoft-pro/workshop-1.git
cd workshop-1

# 2. Enter the Nix development shell
nix develop

# 3. Start PostgreSQL with Podman
podman-compose up -d
# OR without podman-compose:
podman run -d \
  --name recruitment_dw_postgres \
  -e POSTGRES_DB=recruitment_dw \
  -e POSTGRES_USER=recruitment \
  -e POSTGRES_PASSWORD=recruitment123 \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  --restart unless-stopped \
  postgres:16-alpine

# 4. Wait for database to be ready
podman exec recruitment_dw_postgres pg_isready -U recruitment

# 5. Export database URL
export DB_URL="postgresql://recruitment:recruitment123@localhost:5432/recruitment_dw"

# 6. Run the ETL pipeline
python src/main.py

# 7. Open Jupyter for data profiling
jupyter lab
```

### ETL Pipeline Output

When you run the ETL pipeline, you should see the following output:

```
============================================================
  WORKSHOP 1 — RECRUITMENT DATA WAREHOUSE ETL
============================================================

>>> PHASE 1: EXTRACT
[EXTRACT] Loaded 50,000 rows from data/raw/candidates.csv
[EXTRACT] Columns: ['First Name', 'Last Name', 'Email', 'Application Date', 'Country', 'YOE', 'Seniority', 'Technology', 'Code Challenge Score', 'Technical Interview Score']

>>> PHASE 2: TRANSFORM
[TRANSFORM] Prepared 50,000 rows after cleaning
[TRANSFORM] Applied business rule: 6,698/50,000 hired (13.4%)

>>> PHASE 3: DIMENSIONAL MODEL
[DIM] Created dim_date: 1,646 rows
[DIM] Created dim_technology: 24 rows
[DIM] Created dim_candidate: 50,000 rows
[DIM] Created dim_assessment: 121 rows
[FACT] Created fact_applications: 50,000 rows

>>> PHASE 4: LOAD
[LOAD] Connected to PostgreSQL: localhost:5432/recruitment_dw
[LOAD] Schema created successfully
[LOAD] Loaded dim_date: 1,646 rows
[LOAD] Loaded dim_technology: 24 rows
[LOAD] Loaded dim_candidate: 50,000 rows
[LOAD] Loaded dim_assessment: 121 rows
[LOAD] Loaded fact_applications: 50,000 rows

>>> PHASE 5: VALIDATE

[VALIDATE] === Row Counts ===
  dim_date: 1,646 rows
  dim_technology: 24 rows
  dim_candidate: 50,000 rows
  dim_assessment: 121 rows
  fact_applications: 50,000 rows

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

### Exporting Analytical Results

After running the ETL pipeline, export the analytical query results to CSV.

**Linux/macOS:**
```bash
scripts/export_results.sh
```

**Windows:**
```cmd
scripts\export_results.bat
```

Expected output:

```
[EXPORT] R1_hiring_trends
[EXPORT] R2_technology_analysis
[EXPORT] R3_candidate_profile
[EXPORT] R4_geographic_analysis
[EXPORT] R5_assessment_analysis

[EXPORT] Done. Files saved in results/
```

Generated files:

| File | Description |
|------|-------------|
| `R1_hiring_trends.csv` | Monthly/quarterly hiring trends (2018-2022) |
| `R2_technology_analysis.csv` | Hiring rates by technology domain |
| `R3_candidate_profile.csv` | Hiring rates by seniority and experience range |
| `R4_geographic_analysis.csv` | Top 20 countries by recruitment activity |
| `R5_assessment_analysis.csv` | Score distribution matrix for both assessments |

### Managing the Database Container

```bash
# Stop the container
podman stop recruitment_dw_postgres

# Start the container
podman start recruitment_dw_postgres

# Remove the container (data persists in volume)
podman rm recruitment_dw_postgres

# Remove container and volume (deletes all data)
podman rm -v recruitment_dw_postgres

# Connect to the database
psql -h localhost -U recruitment -d recruitment_dw

# View container logs
podman logs recruitment_dw_postgres
```

### Connecting with DBeaver

Create a new PostgreSQL connection with the following settings:

| Setting | Value |
|---------|-------|
| **Host** | `localhost` |
| **Port** | `5432` |
| **Database** | `recruitment_dw` |
| **Username** | `recruitment` |
| **Password** | `recruitment123` |

> If you changed environment variables in a `.env` file, use those values instead.

### Connecting Power BI (Windows VM) to PostgreSQL (Linux Host)

If you are running Power BI Desktop on a Windows virtual machine and PostgreSQL is running on a Linux host, follow these steps to establish the connection.

#### Prerequisites

- Power BI Desktop installed on the Windows VM
- PostgreSQL running on the Linux host (via Podman/Docker)
- Network connectivity between the VM and the Linux host

#### Step 1: Find the Linux Host IP Address

On the Linux host, run:

```bash
ip addr show virbr0 2>/dev/null || ip addr show | grep "inet " | grep -v 127.0.0.1
```

The default libvirt/virbr0 network IP is typically `192.168.122.1`.

#### Step 2: Configure the Connection in Power BI

1. Open **Power BI Desktop** on the Windows VM
2. Click **Get Data** → **More...**
3. Select **PostgreSQL database** and click **Connect**
4. Enter the connection settings:

| Setting | Value |
|---------|-------|
| **Server** | `<LINUX_HOST_IP>:5432` (e.g., `192.168.122.1:5432`) |
| **Database** | `recruitment_dw` |
| **Data Connectivity mode** | `Import` (recommended for development) or `DirectQuery` |

5. Click **OK**

#### Step 3: Authenticate

In the authentication dialog:

| Tab | Setting | Value |
|-----|---------|-------|
| **Database** | Username | `recruitment` |
| **Database** | Password | `recruitment123` |

6. Click **Connect**

#### Step 4: Handle SSL/Certificate Warnings

If Windows prompts to install the Npgsql connector or reports missing SSL certificates:

- Accept the warning for unencrypted connection on the internal virtual network
- This is safe for local/development environments

#### Step 5: Select Tables

1. In the Navigator, expand the `public` schema
2. Select the tables you want to import (e.g., `fact_applications`, `dim_date`, `dim_technology`, `dim_candidate`, `dim_assessment`)
3. Click **Load** or **Transform Data** if you need to clean the data first

#### Connection Summary

| Component | Value |
|-----------|-------|
| **Server IP** | `192.168.122.1` (default virbr0) or your host IP |
| **Port** | `5432` |
| **Database** | `recruitment_dw` |
| **Username** | `recruitment` |
| **Password** | `recruitment123` |
| **SSL Mode** | `Prefer` or `Disable` (for local VMs) |

> **Note:** If the connection fails, ensure the PostgreSQL container is bound to `0.0.0.0:5432` (not just `127.0.0.1:5432`) so it accepts external connections. The `docker-compose.yml` in this project already configures this correctly.

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
│  (PostgreSQL)    │     - Load fact table last
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
| PostgreSQL | Data Warehouse | 16 |
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
