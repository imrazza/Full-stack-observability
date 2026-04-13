from fastapi import FastAPI
import time
import random

from prometheus_client import Histogram, generate_latest
from fastapi.responses import Response

# ---- JAEGER / OTEL ----
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

app = FastAPI()

# -------- Prometheus metric ----------
REQUEST_TIME = Histogram(
    "http_request_duration_seconds",
    "Request latency"
)

# -------- Jaeger tracing -------------
trace.set_tracer_provider(
    TracerProvider(
        resource=Resource.create({SERVICE_NAME: "fastapi-app"})
    )
)

otlp_exporter = OTLPSpanExporter(
    endpoint="http://jaeger:4318/v1/traces"
)

span_processor = BatchSpanProcessor(otlp_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

FastAPIInstrumentor.instrument_app(app)

# -------- Routes ----------
@app.get("/")
def home():
    with REQUEST_TIME.time():
        time.sleep(random.uniform(0.1, 1.0))
        return {"message": "Hello"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
