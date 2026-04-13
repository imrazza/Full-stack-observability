from fastapi import FastAPI
import time
import random

from prometheus_client import Histogram, generate_latest
from fastapi.responses import Response

app = FastAPI()

REQUEST_TIME = Histogram(
    "http_request_duration_seconds",
    "Request latency"
)

@app.get("/")
def home():
    with REQUEST_TIME.time():
        time.sleep(random.uniform(0.1, 1.2))
        return {"message": "Hello"}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
