import tempfile
import os
import src.data as data
import src.features as features
import src.model as model_mod


def test_end_to_end_small():
    df = data.generate_synthetic_trends(n_days=60, seed=123)
    df_feat = features.prepare_features(df)
    feature_cols = [c for c in df_feat.columns if c != "target_up"]
    model, metrics = model_mod.train_model(df_feat, feature_cols)
    assert metrics["accuracy"] >= 0.0  # trivial check: metric exists
    # Save and load
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "m.joblib")
        model_mod.save_model(model, path)
        loaded = model_mod.load_model(path)
        assert loaded is not None
