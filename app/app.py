from flask import Flask
import logging
from prometheus_client import Counter, generate_latest, start_http_server
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Init tracing
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer(__name__)
otlp_exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Init Flask
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Metrics
REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')
start_http_server(8000)

@app.route("/")
def hello():
    REQUESTS.inc()
    logging.info("Hello endpoint hit")
    with tracer.start_as_current_span("hello-span"):
        return "Hello from Observability App!"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.run(host='0.0.0.0', port=5000)
