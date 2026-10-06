

import pandas as pd

POLLUTANTS = ["AQI", "PM2.5", "PM10", "O3", "NO2", "SO2", "CO"]


def summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns count, mean, std, min, 25/50/75th percentiles and max for
    every pollutant column — i.e. df[POLLUTANTS].describe(), transposed
    for readability.
    """
    cols = [c for c in POLLUTANTS if c in df.columns]
    return df[cols].describe().T


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Pearson correlation between all pollutant/AQI columns."""
    cols = [c for c in POLLUTANTS if c in df.columns]
    return df[cols].corr()


def most_correlated_with_aqi(df: pd.DataFrame) -> pd.Series:
    """Which pollutant tracks AQI most closely, ranked descending."""
    corr = correlation_matrix(df)["AQI"].drop("AQI")
    return corr.sort_values(ascending=False)


def variability_by_city(df: pd.DataFrame, column: str = "AQI") -> pd.DataFrame:
    """
    Standard deviation and mean of `column` per city — useful for
    spotting cities with wildly fluctuating air quality vs. stable ones.
    """
    grouped = df.groupby("City")[column].agg(["mean", "std", "min", "max", "count"])
    return grouped.sort_values("std", ascending=False)


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import load_data
    from src.data_cleaning import clean_data

    df = clean_data(load_data("data/raw/aqi_data.csv"))
    print(summary_statistics(df))
    print("\nCorrelation with AQI:\n", most_correlated_with_aqi(df))
