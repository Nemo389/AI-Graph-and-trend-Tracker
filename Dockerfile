FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
# Expose a default port; runtime will override via $PORT on platforms like Render
EXPOSE 8000
# Use shell form to allow environment variable interpolation so Render's $PORT is respected
CMD ["sh","-lc","python -m src.scripts.run_server --host 0.0.0.0 --port ${PORT:-8000}"]
