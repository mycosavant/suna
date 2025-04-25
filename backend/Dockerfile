FROM python:3.11-slim

WORKDIR /app

# Install Poetry and dependencies
COPY pyproject.toml poetry.lock* ./
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-dev

# Install Gunicorn separately (if not managed by Poetry, or for specific version control)
# If Gunicorn is in pyproject.toml, this line might be redundant, but keeping for now.
RUN pip install --no-cache-dir gunicorn

# Copy the .env file first - DO NOT COPY .env file in production builds
# COPY .env .

# Copy the backend code
COPY . .

# Set environment variable
ENV PYTHONPATH=/app

ENV ENV_MODE="production"

# Expose the port the app runs on
EXPOSE 8000

# 24 workers
CMD ["gunicorn", "api:app", "--workers", "24", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout", "600", "--graceful-timeout", "300", "--keep-alive", "250", "--max-requests", "0", "--max-requests-jitter", "0", "--forwarded-allow-ips", "*", "--worker-connections", "5000", "--worker-tmp-dir", "/dev/shm", "--preload"]


# TODO: removed the COPY .env . step from the Dockerfile, the .env file will not be present in the built image for staging or production environments. This ensures that the application will rely solely on the environment variables set at runtime. Consider using a different method to manage environment variables.
