"""Simple FastAPI app exposing prediction endpoints."""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import src.data as data_mod
import src.features as features_mod
import src.model as model_mod
import src.data_connectors as connectors
from pathlib import Path

app = FastAPI(title="Trend Predictor")


class PredictRequest(BaseModel):
    ticker: Optional[str] = None
    keyword: Optional[str] = None
    days: int = 180


model = None
ROOT = Path(__file__).resolve().parents[1]


@app.on_event("startup")
def load_default_model():
    global model
    try:
        model = model_mod.load_model("model.joblib")
    except Exception:
        model = None


@app.get("/health")
def health():
    return {"status": "ok", "model_loaded": model is not None}


@app.get("/")
def homepage():
    index = ROOT / "static" / "index.html"
    if index.exists():
        return FileResponse(index)
    raise HTTPException(status_code=404, detail="index not found")


@app.post("/predict")
def predict(req: PredictRequest):
    # fetch price data (fallback to synthetic)
    if req.ticker:
        df = connectors.fetch_price_history(req.ticker, req.days)
    else:
        df = data_mod.generate_synthetic_trends(n_days=req.days)

    df_feat = features_mod.prepare_features(df)
    feature_cols = [c for c in df_feat.columns if c != "target_up"]

    if model is None:
        raise HTTPException(status_code=503, detail="No model available. Train and save a model.joblib first.")

    X = df_feat[feature_cols]
    preds = model.predict_proba(X) if hasattr(model, "predict_proba") else None
    # return last-day prediction
    last_idx = X.index[-1]
    result = {"date": str(last_idx)}
    if preds is not None:
        # probability of class 1
        result["prob_up"] = float(preds[-1, 1])
    else:
        result["pred_up"] = int(model.predict(X.iloc[[-1]])[0])
    return result
