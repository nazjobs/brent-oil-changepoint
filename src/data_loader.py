import pandas as pd
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_and_process_data(filepath, start_date="2010-01-01"):
    """
    Loads Brent Oil data, fixes mixed date formats, and filters by date.

    Args:
        filepath (str): Path to the raw CSV.
        start_date (str): Filter data after this date (YYYY-MM-DD).

    Returns:
        pd.DataFrame: Cleaned dataframe with 'Date' and 'Price'.
    """
    if not os.path.exists(filepath):
        logger.error(f"File not found at: {filepath}")
        raise FileNotFoundError(f"Data file not found: {filepath}")

    try:
        logger.info(f"Loading data from {filepath}...")
        df = pd.read_csv(filepath)

        # Validate columns
        if "Date" not in df.columns or "Price" not in df.columns:
            logger.error("CSV missing required columns: 'Date' or 'Price'")
            raise ValueError("CSV must contain 'Date' and 'Price' columns")

        # 1. Clean the Price column
        df["Price"] = pd.to_numeric(df["Price"], errors="coerce")

        # 2. Handle Mixed Date Formats
        logger.info("Parsing mixed date formats...")
        df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")

        # Check for date parsing failures
        failed_dates = df["Date"].isna().sum()
        if failed_dates > 0:
            logger.warning(f"Failed to parse {failed_dates} date rows. Dropping them.")
            df = df.dropna(subset=["Date"])

        # 3. Sort and Filter
        df = df.sort_values("Date").reset_index(drop=True)

        mask = df["Date"] >= start_date
        df_filtered = df.loc[mask].copy()

        logger.info(
            f"Data filtered: {len(df)} -> {len(df_filtered)} rows (Post-{start_date})."
        )

        # 4. Handle Missing Values
        if df_filtered["Price"].isnull().sum() > 0:
            logger.info("Interpolating missing price values...")
            df_filtered["Price"] = df_filtered["Price"].interpolate(method="linear")

        return df_filtered.reset_index(drop=True)

    except Exception as e:
        logger.critical(f"Critical error in data loading: {e}")
        raise
