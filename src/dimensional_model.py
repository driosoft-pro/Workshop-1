"""
dimensional_model.py — Module for creating the Star Schema dimensional model.
"""

import pandas as pd


def create_dim_date(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the date dimension from Application Date.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared data with 'Application Date' column.

    Returns
    -------
    pd.DataFrame
        Date dimension with surrogate keys.
    """
    dates = df[["Application Date"]].drop_duplicates().copy()
    dates = dates.sort_values("Application Date").reset_index(drop=True)
    dates["date_key"] = range(1, len(dates) + 1)
    dates["full_date"] = dates["Application Date"]
    dates["year"] = dates["Application Date"].dt.year
    dates["quarter"] = dates["Application Date"].dt.quarter
    dates["month"] = dates["Application Date"].dt.month
    dates["month_name"] = dates["Application Date"].dt.month_name()
    dates["day_of_week"] = dates["Application Date"].dt.day_name()
    dates["day_of_month"] = dates["Application Date"].dt.day

    print(f"[DIM] Created dim_date: {len(dates):,} rows")
    return dates


def create_dim_technology(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the technology dimension.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared data with 'Technology' column.

    Returns
    -------
    pd.DataFrame
        Technology dimension with surrogate keys.
    """
    techs = df[["Technology"]].drop_duplicates().copy()
    techs = techs.sort_values("Technology").reset_index(drop=True)
    techs["technology_key"] = range(1, len(techs) + 1)

    print(f"[DIM] Created dim_technology: {len(techs):,} rows")
    return techs


def create_dim_candidate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the candidate dimension.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared data with candidate attributes.

    Returns
    -------
    pd.DataFrame
        Candidate dimension with surrogate keys.
    """
    candidates = df[["First Name", "Last Name", "Email", "Country", "YOE", "Seniority"]].drop_duplicates().copy()
    candidates = candidates.sort_values(["Last Name", "First Name"]).reset_index(drop=True)
    candidates["candidate_key"] = range(1, len(candidates) + 1)

    print(f"[DIM] Created dim_candidate: {len(candidates):,} rows")
    return candidates


def create_dim_assessment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create the assessment dimension with score combinations.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared data with score columns.

    Returns
    -------
    pd.DataFrame
        Assessment dimension with surrogate keys.
    """
    assessments = df[["Code Challenge Score", "Technical Interview Score"]].drop_duplicates().copy()
    assessments = assessments.sort_values(["Code Challenge Score", "Technical Interview Score"]).reset_index(drop=True)
    assessments["assessment_key"] = range(1, len(assessments) + 1)

    print(f"[DIM] Created dim_assessment: {len(assessments):,} rows")
    return assessments


def create_fact_applications(
    df: pd.DataFrame,
    dim_date: pd.DataFrame,
    dim_technology: pd.DataFrame,
    dim_candidate: pd.DataFrame,
    dim_assessment: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create the fact table by mapping surrogate keys from dimensions.

    Parameters
    ----------
    df : pd.DataFrame
        Prepared data with business rules applied.
    dim_date, dim_technology, dim_candidate, dim_assessment : pd.DataFrame
        Dimension tables with surrogate keys.

    Returns
    -------
    pd.DataFrame
        Fact table with foreign keys and measures.
    """
    fact = df.copy()

    date_map = dim_date.set_index("Application Date")["date_key"].to_dict()
    fact["date_key"] = fact["Application Date"].map(date_map)

    tech_map = dim_technology.set_index("Technology")["technology_key"].to_dict()
    fact["technology_key"] = fact["Technology"].map(tech_map)

    candidate_map = (
        dim_candidate.set_index(["First Name", "Last Name", "Email", "Country", "YOE", "Seniority"])["candidate_key"]
        .to_dict()
    )
    fact["candidate_key"] = fact.apply(
        lambda row: candidate_map.get(
            (row["First Name"], row["Last Name"], row["Email"], row["Country"], row["YOE"], row["Seniority"])
        ),
        axis=1,
    )

    assessment_map = (
        dim_assessment.set_index(["Code Challenge Score", "Technical Interview Score"])["assessment_key"].to_dict()
    )
    fact["assessment_key"] = fact.apply(
        lambda row: assessment_map.get((row["Code Challenge Score"], row["Technical Interview Score"])),
        axis=1,
    )

    fact["application_count"] = 1

    fact = fact[
        [
            "date_key",
            "technology_key",
            "candidate_key",
            "assessment_key",
            "is_hired",
            "code_challenge_score",
            "technical_interview_score",
            "application_count",
        ]
    ].copy()

    fact["code_challenge_score"] = df["Code Challenge Score"].values
    fact["technical_interview_score"] = df["Technical Interview Score"].values

    print(f"[FACT] Created fact_applications: {len(fact):,} rows")
    return fact
