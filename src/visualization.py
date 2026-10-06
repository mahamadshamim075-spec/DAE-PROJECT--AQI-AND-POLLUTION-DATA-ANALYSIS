"""
visualization.py
------------------
Generates charts from the cleaned/analyzed AQI data and saves them as
PNG files into outputs/graphs/. Uses matplotlib + seaborn.
"""

import os

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid")

OUTPUT_DIR = "outputs/graphs"


def _ensure_output_dir(path: str = OUTPUT_DIR):
    os.makedirs(path, exist_ok=True)


def plot_aqi_distribution(df: pd.DataFrame, output_dir: str = OUTPUT_DIR):
    """Histogram of AQI values across all readings."""
    _ensure_output_dir(output_dir)
    plt.figure(figsize=(9, 5))
    sns.histplot(df["AQI"].dropna(), bins=30, kde=True, color="steelblue")
    plt.title("Distribution of AQI Readings")
    plt.xlabel("AQI")
    plt.ylabel("Number of Stations")
    plt.tight_layout()
    path = os.path.join(output_dir, "aqi_distribution.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[visualization] Saved {path}")


def plot_top_cities(df: pd.DataFrame, top_n: int = 10, output_dir: str = OUTPUT_DIR):
    """Horizontal bar chart of the worst average-AQI cities."""
    _ensure_output_dir(output_dir)
    ranked = (
        df.groupby("City")["AQI"].mean().sort_values(ascending=False).head(top_n)
    )
    plt.figure(figsize=(9, 6))
    sns.barplot(x=ranked.values, y=ranked.index, hue=ranked.index,
                palette="Reds_r", legend=False)
    plt.title(f"Top {top_n} Cities by Average AQI (Worst Air Quality)")
    plt.xlabel("Average AQI")
    plt.ylabel("City")
    plt.tight_layout()
    path = os.path.join(output_dir, "top_cities_aqi.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[visualization] Saved {path}")


def plot_pollutant_correlation(df: pd.DataFrame, output_dir: str = OUTPUT_DIR):
    """Heatmap of correlations between AQI and individual pollutants."""
    _ensure_output_dir(output_dir)
    cols = [c for c in ["AQI", "PM2.5", "PM10", "O3", "NO2", "SO2", "CO"]
            if c in df.columns]
    corr = df[cols].corr()

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0)
    plt.title("Correlation Between Pollutants and AQI")
    plt.tight_layout()
    path = os.path.join(output_dir, "pollutant_correlation.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[visualization] Saved {path}")


def plot_aqi_category_distribution(df: pd.DataFrame, output_dir: str = OUTPUT_DIR):
    """Pie/bar chart of how many readings fall into each AQI health category."""
    _ensure_output_dir(output_dir)
    if "AQI_Category" not in df.columns:
        raise ValueError("Run analysis.add_aqi_category(df) before plotting this.")

    counts = df["AQI_Category"].value_counts()
    plt.figure(figsize=(8, 5))
    sns.barplot(x=counts.index, y=counts.values, hue=counts.index,
                palette="viridis", legend=False)
    plt.title("AQI Health Category Distribution")
    plt.ylabel("Number of Readings")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = os.path.join(output_dir, "aqi_category_distribution.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[visualization] Saved {path}")


def plot_monthly_trend(trend_df: pd.DataFrame, output_dir: str = OUTPUT_DIR):
    """Line chart of average AQI over time (expects analysis.monthly_trend output)."""
    _ensure_output_dir(output_dir)
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=trend_df, x="Month", y="Average_AQI", marker="o")
    plt.title("Average AQI Over Time")
    plt.xlabel("Month")
    plt.ylabel("Average AQI")
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = os.path.join(output_dir, "monthly_aqi_trend.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"[visualization] Saved {path}")


def generate_all_visuals(df: pd.DataFrame, output_dir: str = OUTPUT_DIR):
    """Convenience function: generate every chart in one call."""
    from src.analysis import add_aqi_category, monthly_trend

    if "AQI_Category" not in df.columns:
        df = add_aqi_category(df)

    plot_aqi_distribution(df, output_dir)
    plot_top_cities(df, output_dir=output_dir)
    plot_pollutant_correlation(df, output_dir)
    plot_aqi_category_distribution(df, output_dir)
    plot_monthly_trend(monthly_trend(df), output_dir)


if __name__ == "__main__":
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.data_loader import load_data
    from src.data_cleaning import clean_data

    df = clean_data(load_data("data/raw/aqi_data.csv"))
    generate_all_visuals(df)
