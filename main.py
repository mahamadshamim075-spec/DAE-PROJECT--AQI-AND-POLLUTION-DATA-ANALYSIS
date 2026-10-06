


import os
import sys




sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analysis import (
    add_aqi_category,
    dominant_pollutant,
    city_rankings,
    category_distribution,
    monthly_trend,
)
from src.statistics import summary_statistics, most_correlated_with_aqi
from src.visualization import generate_all_visuals

RAW_DATA_PATH = "data/raw/aqi_data.csv"
CLEANED_DATA_PATH = "data/cleaned/cleaned_aqi_data.csv"
REPORT_PATH = "outputs/report.txt"


def build_report(df, worst_cities, best_cities, category_counts, top_corr) -> str:
    lines = []
    lines.append("AQI & POLLUTION DATA ANALYSIS — SUMMARY REPORT")
    lines.append("=" * 50)
    lines.append(f"Total stations/readings analyzed: {len(df)}")
    lines.append(f"Unique cities: {df['City'].nunique()}")
    lines.append(f"Overall average AQI: {df['AQI'].mean():.1f}")
    lines.append(f"Overall median AQI: {df['AQI'].median():.1f}")
    lines.append("")

    lines.append("TOP 10 WORST AIR QUALITY CITIES (highest avg AQI)")
    lines.append("-" * 50)
    for _, row in worst_cities.iterrows():
        lines.append(f"  {row['City']:<40} {row['Average_AQI']:.1f}")
    lines.append("")

    lines.append("TOP 10 BEST AIR QUALITY CITIES (lowest avg AQI)")
    lines.append("-" * 50)
    for _, row in best_cities.iterrows():
        lines.append(f"  {row['City']:<40} {row['Average_AQI']:.1f}")
    lines.append("")

    lines.append("AQI HEALTH CATEGORY DISTRIBUTION")
    lines.append("-" * 50)
    for category, count in category_counts.items():
        lines.append(f"  {category:<35} {count}")
    lines.append("")

    lines.append("POLLUTANT MOST CORRELATED WITH AQI")
    lines.append("-" * 50)
    for pollutant, corr_val in top_corr.items():
        lines.append(f"  {pollutant:<10} r = {corr_val:.3f}")
    lines.append("")

    lines.append("Charts saved to outputs/graphs/:")
    lines.append("  - aqi_distribution.png")
    lines.append("  - top_cities_aqi.png")
    lines.append("  - pollutant_correlation.png")
    lines.append("  - aqi_category_distribution.png")
    lines.append("  - monthly_aqi_trend.png")

    return "\n".join(lines)


def main():
    print("Step 1/6: Loading raw data...")
    raw_df = load_data(RAW_DATA_PATH)

    print("Step 2/6: Cleaning data...")
    clean_df = clean_data(raw_df)

    print("Step 3/6: Saving cleaned dataset...")
    os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)
    clean_df.to_csv(CLEANED_DATA_PATH, index=False)

    print("Step 4/6: Running analysis...")
    clean_df = add_aqi_category(clean_df)
    clean_df = dominant_pollutant(clean_df)
    worst_cities = city_rankings(clean_df, ascending=False, top_n=10)
    best_cities = city_rankings(clean_df, ascending=True, top_n=10)
    categories = category_distribution(clean_df)
    trend = monthly_trend(clean_df)

    print("Step 5/6: Computing statistics...")
    stats = summary_statistics(clean_df)
    top_corr = most_correlated_with_aqi(clean_df)
    print(stats)

    print("Step 6/6: Generating visualizations + report...")
    generate_all_visuals(clean_df)

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    report_text = build_report(clean_df, worst_cities, best_cities, categories, top_corr)
    with open(REPORT_PATH, "w") as f:
        f.write(report_text)

    print("\nDone. Report written to", REPORT_PATH)
    print(report_text)


if __name__ == "__main__":
    main()
