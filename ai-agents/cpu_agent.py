# ai-agents/cpu_agent.py

import random
import time
from datetime import datetime

CPU_THRESHOLD = 80.0  # percent

def get_cpu_metrics():
    """
    Simulates fetching CPU usage per pod.
    Replace with real Prometheus API call in production.
    """
    pods = ["frontend", "backend", "mysql"]
    metrics = {}
    for pod in pods:
        metrics[pod] = round(random.uniform(10, 100), 2)
    return metrics

def fetch_from_prometheus(prometheus_url="http://localhost:9090"):
    """
    Real Prometheus query (use when connected).
    """
    try:
        import requests
        query = "sum(rate(container_cpu_usage_seconds_total[1m])) by (pod)"
        response = requests.get(f"{prometheus_url}/api/v1/query", params={"query": query})
        data = response.json()
        metrics = {}
        for result in data["data"]["result"]:
            pod = result["metric"].get("pod", "unknown")
            value = float(result["value"][1]) * 100  # convert to percent
            metrics[pod] = round(value, 2)
        return metrics
    except Exception as e:
        print(f"[CPU Agent] Prometheus unavailable: {e}. Using simulated data.")
        return get_cpu_metrics()

def analyze_cpu(metrics):
    """
    Detects abnormal CPU spikes across pods.
    Returns list of alerts.
    """
    alerts = []
    for p
