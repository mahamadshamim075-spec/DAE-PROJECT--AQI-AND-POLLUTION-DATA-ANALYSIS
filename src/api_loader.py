

import os
from datetime import datetime
from typing import List

import pandas as pd
import requests

WAQI_BASE_URL = "https://api.waqi.info/feed"


def _get_token() -> str:
    token = os.environ.get("WAQI_API_TOKEN")
    if not token:
        raise EnvironmentError(
            "WAQI_API_TOKEN environment variable not set. "
            "Get a free token at https://aqicn.org/data-platform/token/"
        )
    return token


def fetch_city_aqi(city: str, token: str = None) -> dict:
 
    token = token or _get_token()
    url = f"{WAQI_BASE_URL}/{city}/"
    response = requests.get(url, params={"token": token}, timeout=10)
    response.raise_for_status()
    payload = response.json()

    if payload.get("status") != "ok":
        raise ValueError(f"API error for city '{city}': {payload}")

    data = payload["data"]
    iaqi = data.get("iaqi", {})

    def _val(key):
        return iaqi.get(key, {}).get("v")

    return {
        "City": data.get("city", {}).get("name", city),
        "AQI": data.get("aqi"),
        "PM2.5": _val("pm25"),
        "PM10": _val("pm10"),
        "O3": _val("o3"),
        "NO2": _val("no2"),
        "SO2": _val("so2"),
        "CO": _val("co"),
        "Latitude": data.get("city", {}).get("geo", [None, None])[0],
        "Longitude": data.get("city", {}).get("geo", [None, None])[1],
        "Time": data.get("time", {}).get("s", datetime.now().isoformat()),
    }


def fetch_multiple_cities(cities: List[str], token: str = None) -> pd.DataFrame:
    
    token = token or _get_token()
    records = []
    for city in cities:
        try:
            records.append(fetch_city_aqi(city, token))
        except Exception as exc:  # noqa: BLE001 - report and continue
            print(f"[api_loader] Skipping '{city}': {exc}")

    df = pd.DataFrame(records)
    print(f"[api_loader] Fetched live data for {len(df)}/{len(cities)} cities")
    return df


if __name__ == "__main__":
    # Quick manual test (requires WAQI_API_TOKEN + network access)
    sample_cities = ["Hyderabad", "Delhi", "Mumbai"]
    live_df = fetch_multiple_cities(sample_cities)
    print(live_df)
