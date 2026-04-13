# Full-Stack Observability Platform

A containerized observability stack to monitor microservices using Prometheus, Grafana, and Jaeger. Provides metrics, alerting, dashboards, and distributed tracing for real-time visibility.

## Tech Stack
- Prometheus  
- Grafana  
- Jaeger  
- Docker  
- Node Exporter  
- FastAPI  

## Features
- Metrics scraping with Prometheus  
- CPU and memory monitoring using Node Exporter  
- Request latency tracking  
- Alert rules for CPU, memory, and latency thresholds  
- Grafana dashboards for visualization  
- Distributed tracing with Jaeger  

## Project Structure
full-stack-observability/
├── docker-compose.yml

├── prometheus.yml

├── alerts.yml

└── app/

├── main.py

└── Dockerfile


## Run the Project

docker compose up --build
Access Services
App: http://localhost:8000
Prometheus: http://localhost:9091
Grafana: http://localhost:3001
Jaeger: http://localhost:16686

Grafana Login:
admin / admin


Summary

Built a full-stack observability platform using Prometheus, Grafana, and Jaeger to monitor containerized services, configure alerts, visualize metrics, and analyze distributed traces.
