"""Run the FastAPI server locally with uvicorn."""
from __future__ import annotations

import argparse
import uvicorn


def main(host: str = "127.0.0.1", port: int = 8000):
    uvicorn.run("src.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    main(args.host, args.port)
