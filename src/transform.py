"""
transform.py — Module for data preparation and business rule transformations.
"""

import pandas as pd


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepare the raw data: fix types, handle missing values, standardize formats.

    Parameters
    ----------
    df : pd.DataFrame
        Raw candidate data.

    Returns
    -------
    pd.DataFrame
        Prepared data ready for business transformations.
    """
    df = df.copy()

    df["Application Date"] = pd.to_datetime(df["Application Date"], errors="coerce")

    df["YOE"] = pd.to_numeric(df["YOE"], errors="coerce").fillna(0).astype(int)
    df["Code Challenge Score"] = pd.to_numeric(df["Code Challenge Score"], errors="coerce").fillna(0).astype(int)
    df["Technical Interview Score"] = pd.to_numeric(df["Technical Interview Score"], errors="coerce").fillna(0).astype(int)

    df["Seniority"] = df["Seniority"].str.strip().str.title()
    df["Technology"] = df["Technology"].str.strip()
    df["Country"] = df["Country"].str.strip()

    df = df.drop_duplicates()

    df = df.dropna(subset=["First Name", "Last Name", "Application Date"])

    print(f"[TRANSFORM] Prepared {len(df):,} rows after cleaning")
    return df


def apply_business_rules(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply the hiring business rule and create derived attributes.

    Business Rule:
        HIRED = (Code Challenge Score >= 7) AND (Technical Interview Score >= 7)

    Parameters
    ----------
    df : pd.DataFrame
        Prepared candidate data.

    Returns
    -------
    pd.DataFrame
        Data with hiring outcome and derived attributes.
    """
    df = df.copy()

    df["is_hired"] = (
        (df["Code Challenge Score"] >= 7) & (df["Technical Interview Score"] >= 7)
    ).astype(int)

    df["experience_range"] = pd.cut(
        df["YOE"],
        bins=[0, 4, 9, 19, float("inf")],
        labels=["0-4 years", "5-9 years", "10-19 years", "20+ years"],
        include_lowest=True,
    )

    hired_count = df["is_hired"].sum()
    total = len(df)
    print(f"[TRANSFORM] Applied business rule: {hired_count:,}/{total:,} hired ({hired_count/total*100:.1f}%)")

    return df


if __name__ == "__main__":
    from extract import extract_candidates

    raw = extract_candidates()
    prepared = prepare_data(raw)
    result = apply_business_rules(prepared)
    print(result[["First Name", "Last Name", "Code Challenge Score", "Technical Interview Score", "is_hired"]].head(10))
