

import os
import xml.etree.ElementTree as ET

import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
  
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    # utf-8-sig handles a possible BOM at the start of the file
    df = pd.read_csv(file_path, encoding="utf-8-sig")
    print(f"[data_loader] Loaded {len(df)} rows from {file_path}")
    return df


def load_xml(file_path: str) -> pd.DataFrame:
   
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"XML file not found: {file_path}")

    tree = ET.parse(file_path)
    root = tree.getroot()

    rows = []
    for record in root:
        row = {child.tag: child.text for child in record}
        rows.append(row)

    df = pd.DataFrame(rows)
    print(f"[data_loader] Loaded {len(df)} rows from {file_path}")
    return df


def load_data(file_path: str) -> pd.DataFrame:
   
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".csv":
        return load_csv(file_path)
    elif ext == ".xml":
        return load_xml(file_path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


if __name__ == "__main__":
    # Quick manual test
    df = load_data("data/raw/aqi_data.csv")
    print(df.head())
    print(df.dtypes)
