import time, random
from flask import Flask
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# Jaeger setup (using OTLP — more stable than old Jaeger exporter)
provider = TracerProvider()
provider.add_span_processor(BatchSpanProcessor(
    OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
))
trace.set_tracer_provider(provider)
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer("myapp")

# Prometheus metrics
REQUEST_COUNT   = Counter("myapp_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("myapp_request_duration_seconds", "Request duration")

@app.route("/")
def home():
    REQUEST_COUNT.labels(endpoint="/").inc()
    with REQUEST_LATENCY.time():
        time.sleep(random.uniform(0.01, 0.3))
    return "App is running!"

@app.route("/slow")
def slow():
    REQUEST_COUNT.labels(endpoint="/slow").inc()
    with tracer.start_as_current_span("slow-operation"):
        time.sleep(random.uniform(0.5, 2.0))
    return "That was slow — check Jaeger!"

@app.route("/error")
def error():
    REQUEST_COUNT.labels(endpoint="/error").inc()
    if random.random() > 0.5:
        return "Something went wrong!", 500
    return "No error this time!"

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
