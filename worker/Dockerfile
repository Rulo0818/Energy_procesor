# Worker usa el mismo código que backend (contexto raíz)
FROM python:3.11-slim

WORKDIR /app

COPY backend/ .
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m -u 1000 worker && chown -R worker:worker /app
USER worker

CMD ["celery", "-A", "app.celery_app", "worker", "-l", "info"]
