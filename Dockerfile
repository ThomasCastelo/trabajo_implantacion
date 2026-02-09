# ============================================
# Stage 1: Builder - Instalar dependencias
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir --user --no-compile -r requirements.txt \
    && find /root/.local -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true \
    && find /root/.local -type f -name '*.pyc' -delete \
    && find /root/.local -type f -name '*.pyo' -delete

# ============================================
# Stage 2: Runtime - Imagen final optimizada
# ============================================
FROM python:3.11-slim

LABEL maintainer="tu-email@example.com" \
      version="1.0" \
      description="FastAPI Museo Dinosaurios"

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN useradd -m -u 1000 fastapi && \
    mkdir -p /app && \
    chown -R fastapi:fastapi /app

WORKDIR /app

COPY --from=builder /root/.local /home/fastapi/.local

COPY . .

RUN chown -R fastapi:fastapi /app

ENV PATH=/home/fastapi/.local/bin:$PATH

USER fastapi

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/').read()" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
