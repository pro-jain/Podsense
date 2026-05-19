#!/bin/bash
# scripts/network_spike.sh
# Simulates network traffic burst

echo "======================================"
echo " PodSense - Network Spike Simulation"
echo "======================================"

TARGET_URL=${1:-"http://localhost:30001"}
REQUESTS=${2:-500}
CONCURRENCY=${3:-50}

echo "[*] Target URL     : $TARGET_URL"
echo "[*] Total Requests : $REQUESTS"
echo "[*] Concurrency    : $CONCURRENCY"
echo ""

# Check if ab (Apache Bench) is available
if command -v ab &> /dev/null; then
    echo "[*] Using Apache Bench for load simulation..."
    ab -n $REQUESTS -c $CONCURRENCY $TARGET_URL
elif command -v curl &> /dev/null; then
    echo "[*] ab not found. Using curl loop..."
    for i in $(seq 1 $REQUESTS); do
        curl -s -o /dev/null $TARGET_URL &
        if (( i % CONCURRENCY == 0 )); then
            wait
            echo "[*] Sent $i requests..."
        fi
    done
    wait
else
    echo "[ERROR] Neither 'ab' nor 'curl' found."
    exit 1
fi

echo ""
echo "[✓] Network spike simulation complete."
echo "[*] Check Grafana network panel for traffic burst."
