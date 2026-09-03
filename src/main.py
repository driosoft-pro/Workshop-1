"""
main.py — Orchestrator for the ETL pipeline.
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")

sys.path.insert(0, str(Path(__file__).parent))

from extract import extract_candidates
from transform import prepare_data, apply_business_rules
from dimensional_model import (
    create_dim_date,
    create_dim_technology,
    create_dim_candidate,
    create_dim_assessment,
    create_fact_applications,
)
from load import (
    get_engine,
    create_schema,
    load_dim_date,
    load_dim_technology,
    load_dim_candidate,
    load_dim_assessment,
    load_fact_applications,
    validate_load,
)


def run_etl(db_url: str = None) -> None:
    """
    Execute the complete ETL pipeline.

    Parameters
    ----------
    db_url : str, optional
        PostgreSQL connection string. If None, reads from DB_URL environment variable.
    """
    print("=" * 60)
    print("  WORKSHOP 1 — RECRUITMENT DATA WAREHOUSE ETL")
    print("=" * 60)

    # ── EXTRACT ──────────────────────────────────────────────
    print("\n>>> PHASE 1: EXTRACT")
    raw_df = extract_candidates()

    # ── TRANSFORM ────────────────────────────────────────────
    print("\n>>> PHASE 2: TRANSFORM")
    prepared_df = prepare_data(raw_df)
    transformed_df = apply_business_rules(prepared_df)

    # ── DIMENSIONAL MODEL ────────────────────────────────────
    print("\n>>> PHASE 3: DIMENSIONAL MODEL")
    dim_date = create_dim_date(transformed_df)
    dim_technology = create_dim_technology(transformed_df)
    dim_candidate = create_dim_candidate(transformed_df)
    dim_assessment = create_dim_assessment(transformed_df)

    fact = create_fact_applications(
        transformed_df,
        dim_date,
        dim_technology,
        dim_candidate,
        dim_assessment,
    )

    # ── LOAD ─────────────────────────────────────────────────
    print("\n>>> PHASE 4: LOAD")
    engine = get_engine(db_url)
    create_schema(engine)

    load_dim_date(engine, dim_date)
    load_dim_technology(engine, dim_technology)
    load_dim_candidate(engine, dim_candidate)
    load_dim_assessment(engine, dim_assessment)
    load_fact_applications(engine, fact)

    # ── VALIDATE ─────────────────────────────────────────────
    print("\n>>> PHASE 5: VALIDATE")
    validate_load(engine)

    print("\n" + "=" * 60)
    print("  ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 60)


if __name__ == "__main__":
    db_url = os.environ.get("DB_URL")
    run_etl(db_url)
