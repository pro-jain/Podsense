#!/bin/bash
# scripts/cpu_stress.sh
# Simulates CPU spike inside a Kubernetes pod

echo "======================================"
echo " PodSense - CPU Stress Test"
echo "======================================"

POD_NAME=${1:-"backend"}
NAMESPACE=${2:-"default"}
DURATION=${3:-60}

echo "[*] Target Pod     : $POD_NAME"
echo "[*] Namespace      : $NAMESPACE"
echo "[*] Duration       : ${DURATION}s"
echo ""

echo "[*] Checking if pod exists..."
kubectl get pod $POD_NAME -n $NAMESPACE > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR] Pod '$POD_NAME' not found in namespace '$NAMESPACE'"
    echo "[INFO]  Available pods:"
    kubectl get pods -n $NAMESPACE
    exit 1
fi

echo "[*] Starting CPU stress for ${DURATION} seconds..."
echo "[*] Watch Grafana dashboard for CPU spike!"
echo ""

kubectl exec -it $POD_NAME -n $NAMESPACE -- /bin/sh -c \
    "apt-get install -y stress > /dev/null 2>&1; stress --cpu 2 --timeout ${DURATION}s"

echo ""
echo "[✓] CPU stress test complete."
echo "[*] Check AI agents for generated alerts."
