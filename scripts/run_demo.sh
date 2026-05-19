#!/bin/bash
# scripts/run_demo.sh
# Full demo runner — use this during video presentation

echo "=============================================="
echo "   PODSENSE — FULL DEMO RUNNER"
echo "=============================================="
echo ""

echo "STEP 1: Checking Minikube status..."
minikube status
echo ""

echo "STEP 2: Listing all running pods..."
kubectl get pods -n default
echo ""

echo "STEP 3: Running AI Orchestrator..."
cd ../ai-agents && python orchestrator.py
echo ""

echo "STEP 4: Triggering CPU stress on backend pod..."
bash ../scripts/cpu_stress.sh backend default 30 &

echo "STEP 5: Triggering Memory stress on backend pod..."
bash ../scripts/memory_stress.sh backend default 128 30 &

wait

echo ""
echo "STEP 6: Re-running AI Orchestrator to detect anomalies..."
python orchestrator.py

echo ""
echo "=============================================="
echo "   DEMO COMPLETE"
echo "=============================================="
