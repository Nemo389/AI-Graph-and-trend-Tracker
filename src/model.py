"""Model training utilities."""
from __future__ import annotations

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from typing import Tuple


def train_model(df: pd.DataFrame, feature_cols: list, target_col: str = "target_up") -> Tuple[RandomForestClassifier, dict]:
    X = df[feature_cols]
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    report = classification_report(y_test, preds, output_dict=True)
    metrics = {"accuracy": acc, "report": report}
    return model, metrics


def save_model(model, path: str) -> None:
    joblib.dump(model, path)


def load_model(path: str):
    return joblib.load(path)
