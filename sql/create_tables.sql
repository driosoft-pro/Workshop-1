-- ============================================================
-- create_tables.sql — Star Schema for Recruitment Data Warehouse
-- ============================================================

-- Dimension: Date
CREATE TABLE IF NOT EXISTS dim_date (
    date_key            INTEGER PRIMARY KEY,
    full_date           DATE NOT NULL,
    year                INTEGER NOT NULL,
    quarter             INTEGER NOT NULL,
    month               INTEGER NOT NULL,
    month_name          VARCHAR(20) NOT NULL,
    day_of_week         VARCHAR(20) NOT NULL,
    day_of_month        INTEGER NOT NULL
);

-- Dimension: Technology
CREATE TABLE IF NOT EXISTS dim_technology (
    technology_key      INTEGER PRIMARY KEY,
    technology_name     VARCHAR(100) NOT NULL
);

-- Dimension: Candidate
CREATE TABLE IF NOT EXISTS dim_candidate (
    candidate_key       INTEGER PRIMARY KEY,
    first_name          VARCHAR(100) NOT NULL,
    last_name           VARCHAR(100) NOT NULL,
    email               VARCHAR(255),
    country             VARCHAR(100),
    yoe                 INTEGER,
    seniority           VARCHAR(50)
);

-- Dimension: Assessment
CREATE TABLE IF NOT EXISTS dim_assessment (
    assessment_key      INTEGER PRIMARY KEY,
    code_challenge_score    INTEGER NOT NULL,
    technical_interview_score INTEGER NOT NULL
);

-- Fact: Applications
CREATE TABLE IF NOT EXISTS fact_applications (
    application_id      SERIAL PRIMARY KEY,
    date_key            INTEGER NOT NULL,
    technology_key      INTEGER NOT NULL,
    candidate_key       INTEGER NOT NULL,
    assessment_key      INTEGER NOT NULL,
    is_hired            INTEGER NOT NULL,
    code_challenge_score    INTEGER NOT NULL,
    technical_interview_score INTEGER NOT NULL,
    application_count   INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (technology_key) REFERENCES dim_technology(technology_key),
    FOREIGN KEY (candidate_key) REFERENCES dim_candidate(candidate_key),
    FOREIGN KEY (assessment_key) REFERENCES dim_assessment(assessment_key)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_applications(date_key);
CREATE INDEX IF NOT EXISTS idx_fact_tech ON fact_applications(technology_key);
CREATE INDEX IF NOT EXISTS idx_fact_candidate ON fact_applications(candidate_key);
CREATE INDEX IF NOT EXISTS idx_fact_assessment ON fact_applications(assessment_key);
CREATE INDEX IF NOT EXISTS idx_fact_hired ON fact_applications(is_hired);
