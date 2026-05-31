# =============================================================================
# src/analysis.py
# Student Housing Market Research — Core Analysis Functions
#
# This module handles all the data loading, cleaning, and calculations.
# Keeping it separate from app.py makes the code easier to read and reuse.
# =============================================================================

import pandas as pd
import numpy as np


# -----------------------------------------------------------------------------
# 1. LOAD DATA
# -----------------------------------------------------------------------------

def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the CSV file into a pandas DataFrame.

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Raw data as a DataFrame.
    """
    df = pd.read_csv(filepath)
    return df


# -----------------------------------------------------------------------------
# 2. CLEAN DATA
# -----------------------------------------------------------------------------

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame:
      - Strip whitespace from text columns
      - Drop rows where critical columns are missing
      - Ensure numeric columns are the correct data type
      - Convert percentage-style columns (occupancy_rate, annual_rent_growth)
        from decimals to readable percentages

    Parameters:
        df (pd.DataFrame): Raw DataFrame.

    Returns:
        pd.DataFrame: Cleaned DataFrame.
    """
    # Strip leading/trailing whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    df[str_cols] = df[str_cols].apply(lambda col: col.str.strip())

    # Drop rows that are missing any of these critical columns
    critical_cols = [
        "city", "student_population", "estimated_student_housing_beds",
        "average_monthly_rent", "occupancy_rate", "annual_rent_growth",
        "average_property_price"
    ]
    df = df.dropna(subset=critical_cols)

    # Make sure numeric columns are stored as numbers (not strings)
    numeric_cols = [
        "student_population", "estimated_student_housing_beds",
        "average_monthly_rent", "occupancy_rate", "annual_rent_growth",
        "median_household_income", "average_property_price",
        "distance_to_campus_miles"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Reset the index so rows are numbered 0, 1, 2, ...
    df = df.reset_index(drop=True)

    return df


# -----------------------------------------------------------------------------
# 3. CALCULATE DERIVED METRICS
# -----------------------------------------------------------------------------

def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add three new columns to the DataFrame:

    1. demand_supply_ratio
       = student_population / estimated_student_housing_beds
       A ratio > 1 means there are more students than available beds,
       indicating HIGH demand pressure (good for landlords/investors).

    2. affordability_ratio
       = (average_monthly_rent * 12) / median_household_income
       This is the share of annual income spent on rent.
       Lower is more affordable for renters, but a slightly higher ratio
       can signal strong rental demand (less risk of vacancies).

    3. investment_attractiveness_score  (0–100 scale)
       A simple composite score built from four sub-scores:
         a) Rent growth score   — higher annual rent growth → better
         b) Occupancy score     — higher occupancy rate → better
         c) Demand-supply score — higher ratio → better (more demand)
         d) Price-to-rent score — lower property price relative to annual
                                  rent → better (faster payback)

       Each sub-score is normalized to 0–1 using min-max scaling,
       then averaged and multiplied by 100.

    Parameters:
        df (pd.DataFrame): Cleaned DataFrame.

    Returns:
        pd.DataFrame: DataFrame with three new metric columns.
    """

    # ── Demand-Supply Ratio ────────────────────────────────────────────────
    df["demand_supply_ratio"] = (
        df["student_population"] / df["estimated_student_housing_beds"]
    ).round(2)

    # ── Affordability Ratio ────────────────────────────────────────────────
    df["affordability_ratio"] = (
        (df["average_monthly_rent"] * 12) / df["median_household_income"]
    ).round(3)

    # ── Investment Attractiveness Score ───────────────────────────────────
    # Helper: min-max normalization turns any column into a 0–1 range
    def minmax(series: pd.Series) -> pd.Series:
        rng = series.max() - series.min()
        if rng == 0:
            return pd.Series([0.5] * len(series), index=series.index)
        return (series - series.min()) / rng

    # Sub-score a: rent growth (higher = better)
    score_rent_growth = minmax(df["annual_rent_growth"])

    # Sub-score b: occupancy rate (higher = better)
    score_occupancy = minmax(df["occupancy_rate"])

    # Sub-score c: demand-supply ratio (higher = better)
    score_demand_supply = minmax(df["demand_supply_ratio"])

    # Sub-score d: price-to-rent ratio (lower price relative to rent = better)
    # We calculate annual rent / property price (gross yield proxy),
    # then normalize so that HIGHER yield = HIGHER score.
    gross_yield = (df["average_monthly_rent"] * 12) / df["average_property_price"]
    score_price_to_rent = minmax(gross_yield)

    # Combine the four sub-scores with equal weights (25% each)
    df["investment_score"] = (
        (score_rent_growth + score_occupancy + score_demand_supply + score_price_to_rent)
        / 4 * 100
    ).round(1)

    return df


# -----------------------------------------------------------------------------
# 4. RANK CITIES
# -----------------------------------------------------------------------------

def rank_cities(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sort cities from highest to lowest investment_score and add a rank column.

    Parameters:
        df (pd.DataFrame): DataFrame with investment_score column.

    Returns:
        pd.DataFrame: Sorted DataFrame with a 'rank' column (1 = best).
    """
    df = df.sort_values("investment_score", ascending=False).reset_index(drop=True)
    df.insert(0, "rank", range(1, len(df) + 1))   # add rank as the first column
    return df


# -----------------------------------------------------------------------------
# 5. FULL PIPELINE (convenience function)
# -----------------------------------------------------------------------------

def run_full_analysis(filepath: str) -> pd.DataFrame:
    """
    Run the complete analysis pipeline in one call:
      load → clean → calculate metrics → rank

    Parameters:
        filepath (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Fully processed and ranked DataFrame.
    """
    df = load_data(filepath)
    df = clean_data(df)
    df = calculate_metrics(df)
    df = rank_cities(df)
    return df
