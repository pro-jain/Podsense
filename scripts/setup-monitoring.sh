#!/bin/bash
# scripts/setup-monitoring.sh
# Run this ONCE to set up Prometheus + Grafana

echo "======================================"
echo " PodSense - Monitoring Stack Setup"
echo "======================================"

echo "[1] Deploying Prometheus..."
kubectl apply -f monitoring/prometheus-deployment.yaml

echo "[2] Deploying Grafana..."
kubectl apply -f monitoring/grafana-deployment.yaml

echo "[3] Waiting for pods to start..."
kubectl wait --for=condition=ready pod -l app=prometheus --timeout=60s
kubectl wait --for=condition=ready pod -l app=grafana --timeout=60s

echo "[4] Getting access URLs..."
echo ""
echo "  Prometheus URL:"
minikube service prometheus-service --url

echo ""
echo "  Grafana URL:"
minikube service grafana-service --url

echo ""
echo "  Grafana Login: admin / admin123"
echo ""
echo "[✓] Monitoring stack ready!"
echo ""
echo "NEXT STEPS:"
echo "  1. Open Grafana URL in browser"
echo "  2. Go to: Connections → Data Sources → Add Prometheus"
echo "  3. URL: http://prometheus-service:9090"
echo "  4. Go to: Dashboards → Import → Upload grafana-dashboard.json"
