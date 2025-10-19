"""Synthetic market/product trend data generator."""
from __future__ import annotations

import numpy as np
import pandas as pd
from typing import Tuple


def generate_synthetic_trends(n_days: int = 365, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic time series data representing product metrics and market signals.

    Columns:
    - date, price, volume, sentiment, promotion

    Returns a DataFrame indexed by date.
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range(end=pd.Timestamp.today().normalize(), periods=n_days)

    # Base signals
    trend = np.linspace(0, 1, n_days)
    seasonal = 0.1 * np.sin(np.linspace(0, 12 * np.pi, n_days))

    price = 50 + 10 * trend + 5 * seasonal + rng.normal(0, 1.5, n_days)
    volume = 200 + 50 * np.sin(np.linspace(0, 4 * np.pi, n_days) + 1.0) + rng.normal(0, 10, n_days)
    sentiment = 0.2 * trend + rng.normal(0, 0.05, n_days)
    promotion = (rng.random(n_days) < 0.05).astype(int)  # occasional promotions

    df = pd.DataFrame(
        {
            "date": dates,
            "price": price,
            "volume": volume,
            "sentiment": sentiment,
            "promotion": promotion,
        }
    )
    df = df.set_index("date")
    return df


def save_synthetic_csv(path: str, n_days: int = 365, seed: int = 42) -> None:
    df = generate_synthetic_trends(n_days=n_days, seed=seed)
    df.to_csv(path)


if __name__ == "__main__":
    df = generate_synthetic_trends(60)
    print(df.head())
