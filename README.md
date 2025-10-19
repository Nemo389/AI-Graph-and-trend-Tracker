# AI Graph and Trend Tracker

Minimal prototype to generate synthetic market/product trend data, create lag/rolling features, train a simple model to predict short-term trend direction, and run a lightweight test.

Quick start

1. Create a virtualenv and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Generate data and train:

```bash
python -m src.scripts.train --output-model model.joblib
```

3. Run tests:

```bash
pytest -q
```

Run the prediction API

1. Start the server (after training or placing a `model.joblib` in the project root):

```bash
source .venv/bin/activate
python -m src.scripts.run_server --host 0.0.0.0 --port 8000
```

2. Health check:

```bash
curl http://127.0.0.1:8000/health
```

3. Predict using a ticker or synthetic data:

```bash
# Use synthetic data
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"days":180}'

# Use a ticker (requires yfinance/network access)
curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"ticker":"AAPL","days":180}'
```


This is a starting point — for production use you'd swap synthetic data for real sources (APIs, CSVs), add more features, logging, monitoring, and experiment tracking.
# AI-Graph-and-trend-Tracker
This is a website integrated with an AI model with a designated role of learning how trends like to flow and grow
