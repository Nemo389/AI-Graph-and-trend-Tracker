"""Feature engineering for time series trends."""
from __future__ import annotations

import pandas as pd
from typing import List


def create_lag_features(df: pd.DataFrame, cols: List[str], lags: List[int]) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        for lag in lags:
            df[f"{col}_lag_{lag}"] = df[col].shift(lag)
    return df


def create_rolling_features(df: pd.DataFrame, cols: List[str], windows: List[int]) -> pd.DataFrame:
    df = df.copy()
    for col in cols:
        for w in windows:
            df[f"{col}_roll_mean_{w}"] = df[col].rolling(window=w, min_periods=1).mean()
            df[f"{col}_roll_std_{w}"] = df[col].rolling(window=w, min_periods=1).std().fillna(0)
    return df


def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    cols = ["price", "volume", "sentiment"]
    df = create_lag_features(df, cols, lags=[1, 2, 3])
    df = create_rolling_features(df, cols, windows=[3, 7])
    # Target: short-term direction (price up next day)
    df["target_up"] = (df["price"].shift(-1) > df["price"]).astype(int)
    df = df.dropna()
    return df


if __name__ == "__main__":
    import src.data as data

    df = data.generate_synthetic_trends(30)
    print(prepare_features(df).head())
