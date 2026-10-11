# syntax=docker/dockerfile:1.7
# Demo Shop: API + web page in one small image. Build from the repository root.
FROM python:3.12.10-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1 PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /srv/backend
RUN useradd --create-home --uid 10001 shop

FROM base AS test
COPY backend/requirements.txt backend/requirements-dev.txt ./
RUN pip install -r requirements-dev.txt
COPY backend ./
COPY data ../data
COPY ui ../ui
USER shop
CMD ["pytest", "-q"]

FROM base AS app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/app ./app
COPY data ../data
COPY ui ../ui
USER shop
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
