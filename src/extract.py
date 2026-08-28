"""
extract.py — Module for extracting raw candidate data from CSV source.
"""

import pandas as pd
from pathlib import Path


def extract_candidates(csv_path: str = "data/raw/candidates.csv") -> pd.DataFrame:
    """
    Read the raw candidates CSV file into a pandas DataFrame.

    Parameters
    ----------
    csv_path : str
        Path to the source CSV file (semicolon-delimited).

    Returns
    -------
    pd.DataFrame
        Raw candidate data.
    """
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found: {csv_path}")

    df = pd.read_csv(path, sep=";", encoding="utf-8")

    print(f"[EXTRACT] Loaded {len(df):,} rows from {csv_path}")
    print(f"[EXTRACT] Columns: {list(df.columns)}")

    return df


if __name__ == "__main__":
    df = extract_candidates()
    print(df.head())
    print(df.info())
