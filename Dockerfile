#############################
# Builder stage
#############################
FROM python:3.11-slim AS builder
ENV POETRY_VERSION=1.8.2 \
	POETRY_VIRTUALENVS_CREATE=false \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1
WORKDIR /app

# System deps (build-essential for bcrypt / psycopg if needed)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

COPY pyproject.toml ./

# Install only main (non-dev) deps into global env
RUN poetry install --no-root --only main --no-interaction --no-ansi

# Export requirements (helps reproducibility in runtime layer)
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --only main

COPY . .

#############################
# Runtime stage
#############################
FROM python:3.11-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	UVICORN_WORKERS=2 \
	PORT=8000
WORKDIR /app

COPY --from=builder /app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy only necessary application source (exclude tests / docs by dockerignore)
COPY app ./app
COPY pyproject.toml README.md ./
# Optional .env (ignore if missing)
RUN if [ -f .env ]; then cp .env .env; fi || true

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --retries=3 CMD curl -fs http://localhost:${PORT}/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

