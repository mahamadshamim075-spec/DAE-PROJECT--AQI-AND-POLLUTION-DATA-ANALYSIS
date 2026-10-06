

import pandas as pd

# US EPA-style AQI breakpoints
AQI_CATEGORIES = [
    (0, 50, "Good"),
    (51, 100, "Moderate"),
    (101, 150, "Unhealthy for Sensitive Groups"),
    (151, 200, "Unhealthy"),
    (201, 300, "Very Unhealthy"),
    (301, 500, "Hazardous"),
]

POLLUTANT_COLUMNS = ["PM2.5", "PM10", "O3", "NO2", "SO2", "CO"]


def categorize_aqi(aqi_value: float) -> str:
    """Map a single AQI number to its health category label."""
    if pd.isna(aqi_value):
        return "Unknown"
    for low, high, label in AQI_CATEGORIES:
        if low <= aqi_value <= high:
            return label
    return "Hazardous" if aqi_value > 500 else "Unknown"


def add_aqi_category(df: pd.DataFrame) -> pd.DataFrame:
    """Add an 'AQI_Category' column to the dataframe."""
    df = df.copy()
    df["AQI_Category"] = df["AQI"].apply(categorize_aqi)
    return df


def dominant_pollutant(df: pd.DataFrame) -> pd.DataFrame:
  
    df = df.copy()
    cols = [c for c in POLLUTANT_COLUMNS if c in df.columns]
    df["Dominant_Pollutant"] = df[cols].idxmax(axis=1)
    return df


def city_rankings(df: pd.DataFrame, ascending: bool = False, top_n: int = 10) -> pd.DataFrame:
   
    ranked = (
        df.groupby("City")["AQI"]
        .mean()
        .sort_values(ascending=ascending)
        .head(top_n)
        .reset_index()
        .rename(columns={"AQI": "Average_AQI"})
    )
    return ranked


def category_distribution(df: pd.DataFrame) -> pd.Series:
    """Count of readings falling into each AQI health category."""
    if "AQI_Category" not in df.columns:
        df = add_aqi_category(df)
    return df["AQI_Category"].value_counts()


def monthly_trend(df: pd.DataFrame, city: str = None) -> pd.DataFrame:
   
    data = df.dropna(subset=["Time"])
    if city:
        data = data[data["City"] == city]

    data = data.set_index("Time")
    trend = data["AQI"].resample("ME").mean().reset_index()
    trend.columns = ["Month", "Average_AQI"]
    return trend


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import load_data
    from src.data_cleaning import clean_data

    df = clean_data(load_data("data/raw/aqi_data.csv"))
    df = add_aqi_category(df)
    df = dominant_pollutant(df)

    print("Worst cities:\n", city_rankings(df, ascending=False))
    print("\nCategory distribution:\n", category_distribution(df))
