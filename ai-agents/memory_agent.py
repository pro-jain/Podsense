# ai-agents/memory_agent.py

import random
from datetime import datetime

MEMORY_THRESHOLD_MB = 500  # MB
LEAK_TREND_COUNT = 3  # consecutive increases = leak suspected

def get_memory_metrics():
    """
    Simulates memory usage per pod in MB.
    Replace with Prometheus API in production.
    """
    pods = ["frontend", "backend", "mysql"]
    metrics = {}
    for pod in pods:
        metrics[pod] = round(random.uniform(100, 800), 2)
    return metrics

def simulate_memory_trend(pod_name, steps=5):
    """
    Simulates a trend (increasing = possible leak).
    """
    trend = []
    base = random.uniform(200, 400)
    for i in range(steps):
        base += random.uniform(-20, 60)  # biased upward to simulate leak
        trend.append(round(base, 2))
    return trend

def detect_memory_leak(trend):
    """
    Returns True if memory is continuously increasing.
    """
    increases = 0
    for i in range(1, len(trend)):
        if trend[i] > trend[i - 1]:
            increases += 1
    return increases >= LEAK_TREND_COUNT

def analyze_memory(metrics):
    """
    Detects high memory usage and leak patterns.
    """
    alerts = []
    for pod, mem in metrics.items():
        trend = simulate_memory_trend(pod)
        leak_detected = detect_memory_leak(trend)

        print(f"[Memory Agent] {pod}: {mem} MB | Trend: {trend}")

        if mem > MEMORY_THRESHOLD_MB:
            alerts.append({
                "pod": pod,
                "memory_mb": mem,
                "status": "HIGH_MEMORY",
                "leak_suspected": leak_detected,
                "message": f"High memory on '{pod}': {mem} MB" +
                           (" — Leak pattern suspected!" if leak_detected else ""),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        elif leak_detected:
            alerts.append({
                "pod": pod,
                "memory_mb": mem,
                "status": "LEAK_SUSPECTED",
                "leak_suspected": True,
                "message": f"Memory leak pattern detected on '{pod}' (trend: {trend})",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

    return alerts

def run_memory_agent():
    print("=" * 50)
    print("[Memory Agent] Starting Memory monitoring...")
    print("=" * 50)

    metrics = get_memory_metrics()

    print("\n[Memory Agent] Current Memory Usage:")
    for pod, val in metrics.items():
        print(f"  {pod}: {val} MB")

    alerts = analyze_memory(metrics)

    if alerts:
        print("\n[Memory Agent] ALERTS GENERATED:")
        for alert in alerts:
            print(f"  ⚠️  {alert['message']}")
    else:
        print("\n[Memory Agent] All pods within normal memory range.")

    return alerts

if __name__ == "__main__":
    run_memory_agent()
