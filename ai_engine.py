import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict

import pandas as pd
from prophet import Prophet


def load_financial_csv(csv_path: str) -> pd.DataFrame:
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")

    df = pd.read_csv(path)
    if "date" not in df.columns or "cash_balance" not in df.columns:
        raise ValueError("CSV must include 'date' and 'cash_balance' columns")

    df = df[["date", "cash_balance"]].dropna()
    df["date"] = pd.to_datetime(df["date"])
    df["y"] = df["cash_balance"].astype(float)
    df = df.rename(columns={"date": "ds"})
    if df.empty:
        raise ValueError("No valid rows found in CSV")

    return df[["ds", "y"]]


def forecast_cash(csv_path: str, periods: int = 6, freq: str = "ME") -> List[Dict[str, float]]:
    df = load_financial_csv(csv_path)
    model = Prophet()
    model.fit(df)

    effective_freq = "ME" if freq.upper() in {"M", "ME", "MS"} else freq
    future = model.make_future_dataframe(periods=periods, freq=effective_freq)
    forecast = model.predict(future)

    results: List[Dict[str, float]] = []
    for _, row in forecast.tail(periods).iterrows():
        results.append({
            "date": row["ds"].strftime("%Y-%m-%d"),
            "forecasted_cash_balance": round(row["yhat"], 2),
            "lower_bound": round(row["yhat_lower"], 2),
            "upper_bound": round(row["yhat_upper"], 2),
        })
    return results
