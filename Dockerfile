FROM python:3.12-slim

# Create a non-root user and group
RUN groupadd -r app && useradd -r -g app app

WORKDIR /app
COPY requirements.txt ./
# Install dependencies as root, then drop privileges
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
# Ensure the non-root user owns the application files
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose a default port; runtime will override via $PORT on platforms like Render
EXPOSE 8000
# Use shell form to allow environment variable interpolation so Render's $PORT is respected
CMD ["sh","-lc","python -m src.scripts.run_server --host 0.0.0.0 --port ${PORT:-8000}"]
