"""Small training script to run end-to-end locally."""
from __future__ import annotations

import argparse
import pandas as pd
import src.data as data
import src.features as features
import src.model as model_mod


def main(output_model: str, days: int):
    df = data.generate_synthetic_trends(n_days=days)
    df_feat = features.prepare_features(df)

    feature_cols = [c for c in df_feat.columns if c != "target_up"]
    model, metrics = model_mod.train_model(df_feat, feature_cols)
    print("Metrics:", metrics["accuracy"]) 
    model_mod.save_model(model, output_model)
    print(f"Saved model to {output_model}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-model", default="model.joblib")
    parser.add_argument("--days", type=int, default=365)
    args = parser.parse_args()
    main(args.output_model, args.days)
