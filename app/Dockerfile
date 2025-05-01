FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install flask prometheus_client opentelemetry-api \
    opentelemetry-sdk opentelemetry-exporter-otlp \
    opentelemetry-instrumentation-flask

CMD ["python", "app.py"]
