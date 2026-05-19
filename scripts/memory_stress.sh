#!/bin/bash
# scripts/memory_stress.sh
# Simulates memory pressure inside a Kubernetes pod

echo "======================================"
echo " PodSense - Memory Stress Test"
echo "======================================"

POD_NAME=${1:-"backend"}
NAMESPACE=${2:-"default"}
MEMORY_MB=${3:-256}
DURATION=${4:-60}

echo "[*] Target Pod     : $POD_NAME"
echo "[*] Namespace      : $NAMESPACE"
echo "[*] Memory to use  : ${MEMORY_MB}MB"
echo "[*] Duration       : ${DURATION}s"
echo ""

echo "[*] Checking if pod exists..."
kubectl get pod $POD_NAME -n $NAMESPACE > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "[ERROR] Pod '$POD_NAME' not found."
    kubectl get pods -n $NAMESPACE
    exit 1
fi

echo "[*] Starting memory stress for ${DURATION} seconds..."
echo "[*] Watch Grafana dashboard for memory spike!"

kubectl exec -it $POD_NAME -n $NAMESPACE -- /bin/sh -c \
    "apt-get install -y stress > /dev/null 2>&1; stress --vm 1 --vm-bytes ${MEMORY_MB}M --timeout ${DURATION}s"

echo ""
echo "[✓] Memory stress test complete."
echo "[*] Check AI agents for memory alerts."
