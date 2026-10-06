

from typing import Iterable

import numpy as np
import pandas as pd

MISSING_TOKENS = ["-", "N/A", "NA", "n/a", "null", "None", ""]

NUMERIC_COLUMNS = ["AQI", "PM2.5", "PM10", "O3", "NO2", "SO2", "CO",
                    "Latitude", "Longitude"]


def _standardize_missing(df: pd.DataFrame) -> pd.DataFrame:
    """Replace all known 'missing value' placeholder strings with NaN."""
    df = df.replace(MISSING_TOKENS, np.nan)
    return df


def _split_location(df: pd.DataFrame) -> pd.DataFrame:
   
    if "City" not in df.columns:
        return df

    parts = df["City"].astype(str).str.split(",")

    def _get(parts_list, idx):
        try:
            return parts_list[idx].strip()
        except (IndexError, AttributeError):
            return np.nan

    df["Station"] = parts.apply(lambda p: _get(p, 0))
    df["City"] = parts.apply(lambda p: _get(p, 1) if len(p) > 2 else _get(p, 0))
    df["Country"] = parts.apply(lambda p: _get(p, -1) if len(p) > 1 else np.nan)
    return df


def _convert_numeric(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    """Coerce given columns to numeric, turning unparseable values into NaN."""
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _parse_time(df: pd.DataFrame) -> pd.DataFrame:
    if "Time" in df.columns:
        df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    return df


def _drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    before = len(df)
    df = df.drop_duplicates()
    removed = before - len(df)
    if removed:
        print(f"[data_cleaning] Removed {removed} exact duplicate rows")
    return df


def _remove_invalid_readings(df: pd.DataFrame) -> pd.DataFrame:
   
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df.loc[df[col] < 0, col] = np.nan
    if "AQI" in df.columns:
        df.loc[df["AQI"] > 500, "AQI"] = np.nan
    return df


def _handle_missing_values(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:
    
    pollutant_cols = [c for c in NUMERIC_COLUMNS if c in df.columns
                       and c not in ("Latitude", "Longitude")]

    if strategy == "drop":
        df = df.dropna(subset=["AQI"])
    else:
        for col in pollutant_cols:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    return df


def clean_data(df: pd.DataFrame, missing_strategy: str = "median") -> pd.DataFrame:
    
    
    df = df.copy()

    df = _standardize_missing(df)
    df = _split_location(df)
    df = _convert_numeric(df, NUMERIC_COLUMNS)
    df = _parse_time(df)
    df = _drop_duplicates(df)
    df = _remove_invalid_readings(df)
    df = _handle_missing_values(df, strategy=missing_strategy)

    df = df.reset_index(drop=True)
    print(f"[data_cleaning] Final cleaned dataset: {len(df)} rows, "
          f"{df.shape[1]} columns")
    return df


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import load_data

    raw = load_data("data/raw/aqi_data.csv")
    cleaned = clean_data(raw)
    cleaned.to_csv("data/cleaned/cleaned_aqi_data.csv", index=False)
    print(cleaned.head())
    print(cleaned.isna().sum())
