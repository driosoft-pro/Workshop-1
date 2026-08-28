"""
load.py — Module for loading dimensional data into PostgreSQL Data Warehouse.
"""

import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path


def get_engine(db_url: str = None):
    """
    Create a SQLAlchemy engine for PostgreSQL.

    Parameters
    ----------
    db_url : str, optional
        PostgreSQL connection string. If None, uses SQLite fallback.

    Returns
    -------
    sqlalchemy.engine.Engine
    """
    if db_url is None:
        db_url = "sqlite:///database/recruitment_dw.db"
        print(f"[LOAD] Using SQLite fallback: {db_url}")

    engine = create_engine(db_url)
    return engine


def create_schema(engine) -> None:
    """
    Create the Data Warehouse schema by executing create_tables.sql.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
    """
    sql_path = Path("sql/create_tables.sql")
    if sql_path.exists():
        with open(sql_path, "r") as f:
            sql_content = f.read()

        with engine.connect() as conn:
            for statement in sql_content.split(";"):
                statement = statement.strip()
                if statement:
                    try:
                        conn.execute(text(statement))
                    except Exception as e:
                        print(f"[LOAD] Warning during schema creation: {e}")
            conn.commit()
        print("[LOAD] Schema created successfully")
    else:
        print("[LOAD] sql/create_tables.sql not found, skipping schema creation")


def load_dim_date(engine, dim_date: pd.DataFrame) -> None:
    """Load date dimension into the Data Warehouse."""
    dim_date_export = dim_date.copy()
    dim_date_export["full_date"] = dim_date_export["full_date"].astype(str)
    dim_date_export.to_sql("dim_date", engine, if_exists="replace", index=False)
    print(f"[LOAD] Loaded dim_date: {len(dim_date_export):,} rows")


def load_dim_technology(engine, dim_technology: pd.DataFrame) -> None:
    """Load technology dimension into the Data Warehouse."""
    dim_technology.to_sql("dim_technology", engine, if_exists="replace", index=False)
    print(f"[LOAD] Loaded dim_technology: {len(dim_technology):,} rows")


def load_dim_candidate(engine, dim_candidate: pd.DataFrame) -> None:
    """Load candidate dimension into the Data Warehouse."""
    dim_candidate.to_sql("dim_candidate", engine, if_exists="replace", index=False)
    print(f"[LOAD] Loaded dim_candidate: {len(dim_candidate):,} rows")


def load_dim_assessment(engine, dim_assessment: pd.DataFrame) -> None:
    """Load assessment dimension into the Data Warehouse."""
    dim_assessment.to_sql("dim_assessment", engine, if_exists="replace", index=False)
    print(f"[LOAD] Loaded dim_assessment: {len(dim_assessment):,} rows")


def load_fact_applications(engine, fact: pd.DataFrame) -> None:
    """Load fact table into the Data Warehouse."""
    fact.to_sql("fact_applications", engine, if_exists="replace", index=False)
    print(f"[LOAD] Loaded fact_applications: {len(fact):,} rows")


def validate_load(engine) -> None:
    """
    Validate the loaded Data Warehouse: check row counts and referential integrity.

    Parameters
    ----------
    engine : sqlalchemy.engine.Engine
    """
    tables = ["dim_date", "dim_technology", "dim_candidate", "dim_assessment", "fact_applications"]

    print("\n[VALIDATE] === Row Counts ===")
    with engine.connect() as conn:
        for table in tables:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
            count = result.scalar()
            print(f"  {table}: {count:,} rows")

    print("\n[VALIDATE] === Referential Integrity ===")
    checks = [
        ("fact_applications.date_key", "dim_date.date_key"),
        ("fact_applications.technology_key", "dim_technology.technology_key"),
        ("fact_applications.candidate_key", "dim_candidate.candidate_key"),
        ("fact_applications.assessment_key", "dim_assessment.assessment_key"),
    ]

    with engine.connect() as conn:
        for fk, pk in checks:
            fk_table, fk_col = fk.split(".")
            pk_table, pk_col = pk.split(".")
            result = conn.execute(
                text(
                    f"SELECT COUNT(*) FROM {fk_table} f "
                    f"LEFT JOIN {pk_table} p ON f.{fk_col} = p.{pk_col} "
                    f"WHERE p.{pk_col} IS NULL"
                )
            )
            orphans = result.scalar()
            status = "OK" if orphans == 0 else f"FAILED ({orphans} orphans)"
            print(f"  {fk} -> {pk}: {status}")

    print("[VALIDATE] Validation complete")
