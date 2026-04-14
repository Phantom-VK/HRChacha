FROM python:3.12-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:0.8.13 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

FROM python:3.12-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv
COPY . .

ENV PATH="/app/.venv/bin:$PATH"

RUN mkdir -p /tmp/logs && chmod 777 /tmp/logs

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--logger.level=error"]
