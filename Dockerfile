FROM python:3.11-slim AS builder

WORKDIR /builder
COPY requirements.txt .

# Install deps system-wide so binaries land in /usr/local/bin
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

FROM python:3.11-slim

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed site-packages and console scripts
COPY --from=builder /usr/local /usr/local
COPY . .

RUN mkdir -p /tmp/logs && chmod 777 /tmp/logs

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--logger.level=error"]
