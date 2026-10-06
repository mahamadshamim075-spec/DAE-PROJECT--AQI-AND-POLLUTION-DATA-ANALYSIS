# AQI & Pollution Data Analysis System

A Python pipeline that loads, cleans, analyzes, and visualizes Air
Quality Index (AQI) and pollution data from Indian monitoring stations.

## Project Structure

```
AQI_Pollution_Analysis/
│
├── data/
│   ├── raw/
│   │   └── aqi_data.csv          # Original, uncleaned dataset
│   └── cleaned/
│       └── cleaned_aqi_data.csv  # Output of the cleaning step
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Loads CSV/XML into a DataFrame
│   ├── api_loader.py             # Optional: pulls live AQI data (WAQI API)
│   ├── data_cleaning.py          # Missing values, duplicates, types
│   ├── analysis.py               # Categorization, rankings, trends
│   ├── statistics.py             # Descriptive stats, correlation
│   └── visualization.py          # Charts saved to outputs/graphs/
│
├── outputs/
│   ├── graphs/                   # Generated PNG charts
│   └── report.txt                # Text summary of findings
│
├── main.py                       # Runs the full pipeline end to end
├── requirements.txt
└── README.md
```

## Dataset

`data/raw/aqi_data.csv` contains readings with the following columns:

| Column      | Description                              |
|-------------|-------------------------------------------|
| City        | "Station, City, Country" (split during cleaning) |
| AQI         | Overall Air Quality Index                 |
| PM2.5       | Fine particulate matter (µg/m³)           |
| PM10        | Coarse particulate matter (µg/m³)         |
| O3          | Ozone                                     |
| NO2         | Nitrogen dioxide                          |
| SO2         | Sulfur dioxide                            |
| CO          | Carbon monoxide                           |
| Latitude    | Station latitude                          |
| Longitude   | Station longitude                         |
| Time        | Timestamp of reading                      |

Known data quality issues handled by `data_cleaning.py`:
- Missing values encoded as `-`, `N/A`, blank
- Duplicate station rows
- Combined location string (station/city/country in one field)
- Sensor-error values (negative readings, AQI > 500)

## Setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Run the entire pipeline (clean → analyze → visualize → report):

```bash
python main.py
```

This will:
1. Load `data/raw/aqi_data.csv`
2. Clean it and save to `data/cleaned/cleaned_aqi_data.csv`
3. Compute rankings, AQI health categories, and monthly trends
4. Save charts to `outputs/graphs/`
5. Write `outputs/report.txt` with a full summary

### Using individual modules

```python
from src.data_loader import load_data
from src.data_cleaning import clean_data
from src.analysis import add_aqi_category, city_rankings

df = clean_data(load_data("data/raw/aqi_data.csv"))
df = add_aqi_category(df)
print(city_rankings(df, ascending=False, top_n=5))  # 5 worst cities
```

### Fetching live data (optional)

```bash
export WAQI_API_TOKEN=your_token_here
python src/api_loader.py
```

## Outputs

- `outputs/graphs/aqi_distribution.png` — histogram of AQI values
- `outputs/graphs/top_cities_aqi.png` — worst cities by average AQI
- `outputs/graphs/pollutant_correlation.png` — correlation heatmap
- `outputs/graphs/aqi_category_distribution.png` — health category counts
- `outputs/graphs/monthly_aqi_trend.png` — AQI over time
- `outputs/report.txt` — plain-text summary of all findings
