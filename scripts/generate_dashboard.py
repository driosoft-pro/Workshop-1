"""
generate_dashboard.py — Generate dashboard_recruitment.pbix using pbix-mcp.

Reads CSV results from results/ and creates a multi-page Power BI dashboard.
Run with: nix develop -c python scripts/generate_dashboard.py
"""

import csv
from pathlib import Path
from pbix_mcp.builder import PBIXBuilder

PROJECT = Path(__file__).parent.parent
RESULTS = PROJECT / "results"
OUTPUT = PROJECT / "dashboard_recruitment.pbix"


def read_csv(filename):
    """Read a CSV file and return list of dicts."""
    rows = []
    with open(RESULTS / filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if not row or all(v is None for v in row.values()):
                continue
            first_val = list(row.values())[0]
            if first_val and first_val.startswith("("):
                continue
            cleaned = {}
            for k, v in row.items():
                if v is None:
                    continue
                try:
                    cleaned[k] = int(v)
                except ValueError:
                    try:
                        cleaned[k] = float(v)
                    except ValueError:
                        cleaned[k] = v
            if cleaned:
                rows.append(cleaned)
    return rows


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

    # ── Load CSV data ─────────────────────────────────────────
    r1_data = read_csv("R1_hiring_trends.csv")
    r2_data = read_csv("R2_technology_analysis.csv")
    r3_data = read_csv("R3_candidate_profile.csv")
    r4_data = read_csv("R4_geographic_analysis.csv")
    r5_data = read_csv("R5_assessment_analysis.csv")

    # ── R1: Hiring Trends ─────────────────────────────────────
    builder.add_table("R1_hiring_trends", [
        {"name": "year", "data_type": "Int64"},
        {"name": "month_name", "data_type": "String"},
        {"name": "total_applications", "data_type": "Int64"},
        {"name": "total_hired", "data_type": "Int64"},
        {"name": "hiring_rate_pct", "data_type": "Double"},
    ], rows=r1_data)

    # ── R2: Technology Analysis ───────────────────────────────
    builder.add_table("R2_technology_analysis", [
        {"name": "technology_name", "data_type": "String"},
        {"name": "total_applications", "data_type": "Int64"},
        {"name": "total_hired", "data_type": "Int64"},
        {"name": "hiring_rate_pct", "data_type": "Double"},
    ], rows=r2_data)

    # ── R3: Candidate Profile ─────────────────────────────────
    builder.add_table("R3_candidate_profile", [
        {"name": "seniority", "data_type": "String"},
        {"name": "experience_range", "data_type": "String"},
        {"name": "total_applications", "data_type": "Int64"},
        {"name": "total_hired", "data_type": "Int64"},
        {"name": "hiring_rate_pct", "data_type": "Double"},
    ], rows=r3_data)

    # ── R4: Geographic Analysis ───────────────────────────────
    builder.add_table("R4_geographic_analysis", [
        {"name": "country", "data_type": "String"},
        {"name": "total_applications", "data_type": "Int64"},
        {"name": "total_hired", "data_type": "Int64"},
        {"name": "hiring_rate_pct", "data_type": "Double"},
    ], rows=r4_data)

    # ── R5: Assessment Analysis ───────────────────────────────
    builder.add_table("R5_assessment_analysis", [
        {"name": "code_challenge_score", "data_type": "Int64"},
        {"name": "technical_interview_score", "data_type": "Int64"},
        {"name": "total_applications", "data_type": "Int64"},
        {"name": "total_hired", "data_type": "Int64"},
    ], rows=r5_data)

    # ── Measures ──────────────────────────────────────────────
    builder.add_measure("R1_hiring_trends", "Total Applications",
                        "SUM(R1_hiring_trends[total_applications])")
    builder.add_measure("R1_hiring_trends", "Total Hired",
                        "SUM(R1_hiring_trends[total_hired])")
    builder.add_measure("R1_hiring_trends", "Hiring Rate",
                        "DIVIDE(SUM(R1_hiring_trends[total_hired]), SUM(R1_hiring_trends[total_applications])) * 100")

    builder.add_measure("R2_technology_analysis", "Total Applications R2",
                        "SUM(R2_technology_analysis[total_applications])")
    builder.add_measure("R2_technology_analysis", "Total Hired R2",
                        "SUM(R2_technology_analysis[total_hired])")
    builder.add_measure("R2_technology_analysis", "Hiring Rate R2",
                        "DIVIDE(SUM(R2_technology_analysis[total_hired]), SUM(R2_technology_analysis[total_applications])) * 100")

    builder.add_measure("R3_candidate_profile", "Total Applications R3",
                        "SUM(R3_candidate_profile[total_applications])")
    builder.add_measure("R3_candidate_profile", "Total Hired R3",
                        "SUM(R3_candidate_profile[total_hired])")
    builder.add_measure("R3_candidate_profile", "Hiring Rate R3",
                        "DIVIDE(SUM(R3_candidate_profile[total_hired]), SUM(R3_candidate_profile[total_applications])) * 100")

    builder.add_measure("R4_geographic_analysis", "Total Applications R4",
                        "SUM(R4_geographic_analysis[total_applications])")
    builder.add_measure("R4_geographic_analysis", "Total Hired R4",
                        "SUM(R4_geographic_analysis[total_hired])")
    builder.add_measure("R4_geographic_analysis", "Hiring Rate R4",
                        "DIVIDE(SUM(R4_geographic_analysis[total_hired]), SUM(R4_geographic_analysis[total_applications])) * 100")

    builder.add_measure("R5_assessment_analysis", "Total Applications R5",
                        "SUM(R5_assessment_analysis[total_applications])")
    builder.add_measure("R5_assessment_analysis", "Total Hired R5",
                        "SUM(R5_assessment_analysis[total_hired])")

    # ── Pages with visuals ────────────────────────────────────

    # Page 1: Overview
    builder.add_page("Overview", [
        vis("card", {"measure": "R1_hiring_trends[Total Applications]"},
            x=20, y=20, width=250, height=150, z=0),
        vis("card", {"measure": "R1_hiring_trends[Total Hired]"},
            x=290, y=20, width=250, height=150, z=1000),
        vis("card", {"measure": "R1_hiring_trends[Hiring Rate]"},
            x=560, y=20, width=250, height=150, z=2000),
        vis("bar_chart", {
            "category": {"table": "R2_technology_analysis", "column": "technology_name"},
            "measure": "R2_technology_analysis[Total Applications R2]",
            "sort": "R2_technology_analysis.technology_name",
        }, x=20, y=200, width=500, height=500, z=3000),
        vis("column_chart", {
            "category": {"table": "R1_hiring_trends", "column": "year"},
            "measure": "R1_hiring_trends[Total Applications]",
        }, x=540, y=200, width=500, height=500, z=4000),
    ])

    # Page 2: R1 - Hiring Trends
    builder.add_page("R1 - Hiring Trends", [
        vis("line_chart", {
            "category": {"table": "R1_hiring_trends", "column": "month_name"},
            "measure": "R1_hiring_trends[Hiring Rate]",
        }, x=20, y=20, width=600, height=350, z=0),
        vis("column_chart", {
            "category": {"table": "R1_hiring_trends", "column": "month_name"},
            "measure": "R1_hiring_trends[Total Applications]",
        }, x=20, y=390, width=600, height=350, z=1000),
        vis("table", {
            "columns": [
                {"table": "R1_hiring_trends", "column": "year"},
                {"table": "R1_hiring_trends", "column": "month_name"},
                {"table": "R1_hiring_trends", "column": "total_applications"},
                {"table": "R1_hiring_trends", "column": "total_hired"},
                {"table": "R1_hiring_trends", "column": "hiring_rate_pct"},
            ],
        }, x=640, y=20, width=500, height=720, z=2000),
    ])

    # Page 3: R2 - Technology Analysis
    builder.add_page("R2 - Technology Analysis", [
        vis("bar_chart", {
            "category": {"table": "R2_technology_analysis", "column": "technology_name"},
            "measure": "R2_technology_analysis[Total Hired R2]",
            "sort": "R2_technology_analysis.technology_name",
        }, x=20, y=20, width=600, height=700, z=0),
        vis("table", {
            "columns": [
                {"table": "R2_technology_analysis", "column": "technology_name"},
                {"table": "R2_technology_analysis", "column": "total_applications"},
                {"table": "R2_technology_analysis", "column": "total_hired"},
                {"table": "R2_technology_analysis", "column": "hiring_rate_pct"},
            ],
        }, x=640, y=20, width=500, height=700, z=1000),
    ])

    # Page 4: R3 - Candidate Profile
    builder.add_page("R3 - Candidate Profile", [
        vis("bar_chart", {
            "category": {"table": "R3_candidate_profile", "column": "seniority"},
            "measure": "R3_candidate_profile[Hiring Rate R3]",
        }, x=20, y=20, width=500, height=350, z=0),
        vis("column_chart", {
            "category": {"table": "R3_candidate_profile", "column": "experience_range"},
            "measure": "R3_candidate_profile[Total Hired R3]",
        }, x=20, y=390, width=500, height=350, z=1000),
        vis("table", {
            "columns": [
                {"table": "R3_candidate_profile", "column": "seniority"},
                {"table": "R3_candidate_profile", "column": "experience_range"},
                {"table": "R3_candidate_profile", "column": "total_applications"},
                {"table": "R3_candidate_profile", "column": "total_hired"},
                {"table": "R3_candidate_profile", "column": "hiring_rate_pct"},
            ],
        }, x=540, y=20, width=600, height=720, z=2000),
    ])

    # Page 5: R4 - Geographic Analysis
    builder.add_page("R4 - Geographic Analysis", [
        vis("bar_chart", {
            "category": {"table": "R4_geographic_analysis", "column": "country"},
            "measure": "R4_geographic_analysis[Total Applications R4]",
            "sort": "R4_geographic_analysis.country",
        }, x=20, y=20, width=500, height=700, z=0),
        vis("table", {
            "columns": [
                {"table": "R4_geographic_analysis", "column": "country"},
                {"table": "R4_geographic_analysis", "column": "total_applications"},
                {"table": "R4_geographic_analysis", "column": "total_hired"},
                {"table": "R4_geographic_analysis", "column": "hiring_rate_pct"},
            ],
        }, x=540, y=20, width=500, height=700, z=1000),
    ])

    # Page 6: R5 - Assessment Analysis
    builder.add_page("R5 - Assessment Analysis", [
        vis("table", {
            "columns": [
                {"table": "R5_assessment_analysis", "column": "code_challenge_score"},
                {"table": "R5_assessment_analysis", "column": "technical_interview_score"},
                {"table": "R5_assessment_analysis", "column": "total_applications"},
                {"table": "R5_assessment_analysis", "column": "total_hired"},
            ],
        }, x=20, y=20, width=500, height=700, z=0),
        vis("column_chart", {
            "category": {"table": "R5_assessment_analysis", "column": "code_challenge_score"},
            "measure": "R5_assessment_analysis[Total Applications R5]",
        }, x=540, y=20, width=500, height=350, z=1000),
        vis("column_chart", {
            "category": {"table": "R5_assessment_analysis", "column": "code_challenge_score"},
            "measure": "R5_assessment_analysis[Total Hired R5]",
        }, x=540, y=390, width=500, height=350, z=2000),
    ])

    # ── Save ──────────────────────────────────────────────────
    builder.save(str(OUTPUT))
    print(f"[OK] Dashboard saved to: {OUTPUT}")
    print(f"[OK] Pages: Overview, R1-R5")
    print(f"[OK] Tables: 5 (R1-R5 analytical results)")
    print(f"[OK] Measures: 14 DAX measures")
    print(f"[OK] Visuals: 18 charts/tables/cards")


if __name__ == "__main__":
    build()
