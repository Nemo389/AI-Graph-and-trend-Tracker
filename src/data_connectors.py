"""Connectors to fetch real market/product trend data.

This module provides light wrappers over yfinance and pytrends. Both are optional
and we gracefully fall back to the synthetic generator in `src.data` when not available
or when network access is disabled.
"""
from __future__ import annotations

from typing import Optional
import pandas as pd

try:
    import yfinance as yf
except Exception:
    yf = None

try:
    from pytrends.request import TrendReq
except Exception:
    TrendReq = None

from datetime import timedelta
import src.data as synthetic


def fetch_price_history(ticker: str, period_days: int = 365) -> pd.DataFrame:
    """Fetch OHLCV price data for `ticker`. Returns DataFrame indexed by date with a `price` column.

    Falls back to synthetic data if yfinance isn't available or fetch fails.
    """
    if yf is None:
        # fallback
        return synthetic.generate_synthetic_trends(n_days=period_days)

    try:
        period = f"{period_days}d"
        hist = yf.Ticker(ticker).history(period=period)
        if hist.empty:
            return synthetic.generate_synthetic_trends(n_days=period_days)
        # use 'Close' as price
        df = pd.DataFrame({"price": hist["Close"], "volume": hist.get("Volume")})
        df.index = pd.to_datetime(df.index).normalize()
        # add placeholder sentiment/promotion
        df["sentiment"] = 0.0
        df["promotion"] = 0
        return df
    except Exception:
        return synthetic.generate_synthetic_trends(n_days=period_days)


def fetch_google_trends(keyword: str, period_days: int = 365) -> pd.DataFrame:
    """Fetch Google Trends interest over time. Returns DataFrame with 'trend' column.

    Falls back to synthetic if pytrends not available.
    """
    if TrendReq is None:
        df = synthetic.generate_synthetic_trends(n_days=period_days)
        return pd.DataFrame({"trend": df["sentiment"]})

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        timeframe = f'today {period_days}-d'
        pytrends.build_payload([keyword], timeframe=timeframe)
        data = pytrends.interest_over_time()
        if data.empty:
            raise RuntimeError("empty trends")
        data = data.reset_index()
        data = data.rename(columns={keyword: "trend"})
        data = data.set_index("date")
        return data[["trend"]]
    except Exception:
        df = synthetic.generate_synthetic_trends(n_days=period_days)
        return pd.DataFrame({"trend": df["sentiment"]})
