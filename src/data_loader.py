import pandas as pd
import numpy as np
import os


def load_and_process_data(filepath, start_date="2010-01-01"):
    """
    Loads Brent Oil data, fixes mixed date formats, and filters by date.

    Args:
        filepath (str): Path to the raw CSV.
        start_date (str): Filter data after this date (YYYY-MM-DD).

    Returns:
        pd.DataFrame: Cleaned dataframe with 'Date' and 'Price'.
    """
    print(f"Loading data from {filepath}...")

    # Load data
    df = pd.read_csv(filepath)

    # 1. Clean the Price column (ensure it's float)
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

    # 2. Handle Mixed Date Formats
    # The dataset has '20-May-87' and '"Nov 08, 2022"'.
    # pd.to_datetime with 'mixed' handles this robustly in pandas 2.0+
    print("Parsing dates (this may take a moment)...")
    df["Date"] = pd.to_datetime(df["Date"], format="mixed")

    # 3. Sort and Filter
    df = df.sort_values("Date").reset_index(drop=True)

    # Filter for the modern era (Business Objective: Relevant Analysis)
    mask = df["Date"] >= start_date
    df_filtered = df.loc[mask].copy()

    print(
        f"Data filtered from {len(df)} to {len(df_filtered)} rows (Post-{start_date})."
    )

    # 4. Handle Missing Values
    if df_filtered.isnull().sum().any():
        print("Interpolating missing values...")
        df_filtered = df_filtered.interpolate(method="linear")

    return df_filtered.reset_index(drop=True)


if __name__ == "__main__":
    # Quick test
    data_path = os.path.join(os.path.dirname(__file__), "../data/BrentOilPrices.csv")
    try:
        df = load_and_process_data(data_path)
        print(df.head())
        print(df.tail())
    except FileNotFoundError:
        print("File not found. Check path.")
