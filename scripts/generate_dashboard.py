"""
generate_dashboard.py — Generate dashboard_recruitment.pbix using pbix-mcp.

Connects to PostgreSQL and creates a multi-page Power BI dashboard.
Run with: nix develop -c python scripts/generate_dashboard.py
"""

from pathlib import Path
from pbix_mcp.builder import PBIXBuilder

PROJECT = Path(__file__).parent.parent
OUTPUT = PROJECT / "dashboard_recruitment.pbix"

# PostgreSQL connection settings
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "recruitment_dw"
DB_USER = "recruitment"
DB_PASS = "recruitment123"


def vis(visual_type, config, x=20, y=20, width=400, height=300, z=0):
    """Create a visual dict for add_page."""
    return {
        "type": visual_type,
        "config": config,
        "x": x, "y": y,
        "width": width, "height": height,
        "z": z,
    }


def build():
    builder = PBIXBuilder()

    db_conn = {
        "type": "postgresql",
        "server": DB_HOST,
        "database": DB_NAME,
        "port": DB_PORT,
        "schema": "public",
        "table": None,  # set per table
    }

    # ── Tables from PostgreSQL (with snapshot data for offline use) ──

    # fact_applications
    builder.add_table("fact_applications", [
        {"name": "application_id", "data_type": "Int64"},
        {"name": "date_key", "data_type": "Int64"},
        {"name": "technology_key", "data_type": "Int64"},
        {"name": "candidate_key", "data_type": "Int64"},
        {"name": "assessment_key", "data_type": "Int64"},
        {"name": "is_hired", "data_type": "Int64"},
        {"name": "code_challenge_score", "data_type": "Int64"},
        {"name": "technical_interview_score", "data_type": "Int64"},
        {"name": "application_count", "data_type": "Int64"},
    ], source_db={**db_conn, "table": "fact_applications"}, mode="directquery")

    # dim_date
    builder.add_table("dim_date", [
        {"name": "date_key", "data_type": "Int64"},
        {"name": "full_date", "data_type": "DateTime"},
        {"name": "year", "data_type": "Int64"},
        {"name": "quarter", "data_type": "Int64"},
        {"name": "month", "data_type": "Int64"},
        {"name": "month_name", "data_type": "String"},
        {"name": "day_of_week", "data_type": "String"},
        {"name": "day_of_month", "data_type": "Int64"},
    ], source_db={**db_conn, "table": "dim_date"}, mode="directquery")

    # dim_technology
    builder.add_table("dim_technology", [
        {"name": "technology_key", "data_type": "Int64"},
        {"name": "technology_name", "data_type": "String"},
    ], source_db={**db_conn, "table": "dim_technology"}, mode="directquery")

    # dim_candidate
    builder.add_table("dim_candidate", [
        {"name": "candidate_key", "data_type": "Int64"},
        {"name": "first_name", "data_type": "String"},
        {"name": "last_name", "data_type": "String"},
        {"name": "email", "data_type": "String"},
        {"name": "country", "data_type": "String"},
        {"name": "yoe", "data_type": "Int64"},
        {"name": "seniority", "data_type": "String"},
    ], source_db={**db_conn, "table": "dim_candidate"}, mode="directquery")

    # dim_assessment
    builder.add_table("dim_assessment", [
        {"name": "assessment_key", "data_type": "Int64"},
        {"name": "code_challenge_score", "data_type": "Int64"},
        {"name": "technical_interview_score", "data_type": "Int64"},
    ], source_db={**db_conn, "table": "dim_assessment"}, mode="directquery")

    # ── Relationships ─────────────────────────────────────────
    builder.add_relationship("fact_applications", "date_key", "dim_date", "date_key")
    builder.add_relationship("fact_applications", "technology_key", "dim_technology", "technology_key")
    builder.add_relationship("fact_applications", "candidate_key", "dim_candidate", "candidate_key")
    builder.add_relationship("fact_applications", "assessment_key", "dim_assessment", "assessment_key")

    # ── Measures (hosted on fact_applications) ────────────────
    builder.add_measure("fact_applications", "Total Applications",
                        "COUNT(fact_applications[application_id])")
    builder.add_measure("fact_applications", "Total Hired",
                        "SUM(fact_applications[is_hired])")
    builder.add_measure("fact_applications", "Hiring Rate",
                        "DIVIDE([Total Hired], [Total Applications]) * 100")
    builder.add_measure("fact_applications", "Avg Code Challenge",
                        "AVERAGE(fact_applications[code_challenge_score])")
    builder.add_measure("fact_applications", "Avg Interview Score",
                        "AVERAGE(fact_applications[technical_interview_score])")

    # ── Pages with visuals ────────────────────────────────────

    # Page 1: Overview
    builder.add_page("Overview", [
        vis("card", {"measure": "fact_applications[Total Applications]"},
            x=20, y=20, width=250, height=150, z=0),
        vis("card", {"measure": "fact_applications[Total Hired]"},
            x=290, y=20, width=250, height=150, z=1000),
        vis("card", {"measure": "fact_applications[Hiring Rate]"},
            x=560, y=20, width=250, height=150, z=2000),
        vis("clusteredBarChart", {
            "category": {"table": "dim_technology", "column": "technology_name"},
            "measure": "fact_applications[Total Applications]",
            "sort": "dim_technology.technology_name",
        }, x=20, y=200, width=500, height=500, z=3000),
        vis("clusteredColumnChart", {
            "category": {"table": "dim_date", "column": "year"},
            "measure": "fact_applications[Total Applications]",
        }, x=540, y=200, width=500, height=500, z=4000),
    ])

    # Page 2: R1 - Hiring Trends
    builder.add_page("R1 - Hiring Trends", [
        vis("lineChart", {
            "category": {"table": "dim_date", "column": "month_name"},
            "measure": "fact_applications[Hiring Rate]",
        }, x=20, y=20, width=600, height=350, z=0),
        vis("clusteredColumnChart", {
            "category": {"table": "dim_date", "column": "month_name"},
            "measure": "fact_applications[Total Applications]",
        }, x=20, y=390, width=600, height=350, z=1000),
        vis("table", {
            "columns": [
                {"table": "dim_date", "column": "year"},
                {"table": "dim_date", "column": "month_name"},
                {"measure": "fact_applications[Total Applications]"},
                {"measure": "fact_applications[Total Hired]"},
                {"measure": "fact_applications[Hiring Rate]"},
            ],
        }, x=640, y=20, width=500, height=720, z=2000),
    ])

    # Page 3: R2 - Technology Analysis
    builder.add_page("R2 - Technology Analysis", [
        vis("clusteredBarChart", {
            "category": {"table": "dim_technology", "column": "technology_name"},
            "measure": "fact_applications[Total Hired]",
            "sort": "dim_technology.technology_name",
        }, x=20, y=20, width=600, height=700, z=0),
        vis("table", {
            "columns": [
                {"table": "dim_technology", "column": "technology_name"},
                {"measure": "fact_applications[Total Applications]"},
                {"measure": "fact_applications[Total Hired]"},
                {"measure": "fact_applications[Hiring Rate]"},
            ],
        }, x=640, y=20, width=500, height=700, z=1000),
    ])

    # Page 4: R3 - Candidate Profile
    builder.add_page("R3 - Candidate Profile", [
        vis("clusteredBarChart", {
            "category": {"table": "dim_candidate", "column": "seniority"},
            "measure": "fact_applications[Hiring Rate]",
        }, x=20, y=20, width=500, height=350, z=0),
        vis("clusteredColumnChart", {
            "category": {"table": "dim_candidate", "column": "seniority"},
            "measure": "fact_applications[Total Hired]",
        }, x=20, y=390, width=500, height=350, z=1000),
        vis("table", {
            "columns": [
                {"table": "dim_candidate", "column": "seniority"},
                {"table": "dim_candidate", "column": "yoe"},
                {"table": "dim_candidate", "column": "country"},
                {"measure": "fact_applications[Total Applications]"},
                {"measure": "fact_applications[Total Hired]"},
                {"measure": "fact_applications[Hiring Rate]"},
            ],
        }, x=540, y=20, width=600, height=720, z=2000),
    ])

    # Page 5: R4 - Geographic Analysis
    builder.add_page("R4 - Geographic Analysis", [
        vis("clusteredBarChart", {
            "category": {"table": "dim_candidate", "column": "country"},
            "measure": "fact_applications[Total Applications]",
            "sort": "dim_candidate.country",
        }, x=20, y=20, width=500, height=700, z=0),
        vis("table", {
            "columns": [
                {"table": "dim_candidate", "column": "country"},
                {"measure": "fact_applications[Total Applications]"},
                {"measure": "fact_applications[Total Hired]"},
                {"measure": "fact_applications[Hiring Rate]"},
            ],
        }, x=540, y=20, width=500, height=700, z=1000),
    ])

    # Page 6: R5 - Assessment Analysis
    builder.add_page("R5 - Assessment Analysis", [
        vis("table", {
            "columns": [
                {"table": "dim_assessment", "column": "code_challenge_score"},
                {"table": "dim_assessment", "column": "technical_interview_score"},
                {"measure": "fact_applications[Total Applications]"},
                {"measure": "fact_applications[Total Hired]"},
            ],
        }, x=20, y=20, width=500, height=700, z=0),
        vis("clusteredColumnChart", {
            "category": {"table": "dim_assessment", "column": "code_challenge_score"},
            "measure": "fact_applications[Total Applications]",
        }, x=540, y=20, width=500, height=350, z=1000),
        vis("clusteredColumnChart", {
            "category": {"table": "dim_assessment", "column": "code_challenge_score"},
            "measure": "fact_applications[Total Hired]",
        }, x=540, y=390, width=500, height=350, z=2000),
    ])

    # ── Save ──────────────────────────────────────────────────
    builder.save(str(OUTPUT))
    print(f"[OK] Dashboard saved to: {OUTPUT}")
    print(f"[OK] Pages: Overview, R1-R5")
    print(f"[OK] Tables: 5 (fact + 4 dimensions)")
    print(f"[OK] Relationships: 4 (FK -> PK)")
    print(f"[OK] Measures: 5 DAX measures")
    print(f"[OK] Visuals: 18 charts/tables/cards")
    print(f"[OK] Mode: DirectQuery (PostgreSQL)")


if __name__ == "__main__":
    build()
