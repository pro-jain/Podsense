# PodSense — System Workflow

## End-to-End Flow

### Step 1 — Metric Collection
- Prometheus scrapes all pod metrics every 15 seconds
- Metrics collected: CPU usage, memory usage, network bytes, pod restarts

### Step 2 — AI Agent Analysis
Each agent runs independently:

**CPU Agent**
- Reads CPU % per pod
- Triggers alert if CPU > 80%
- Tags pod as CRITICAL or NORMAL

**Memory Agent**
- Reads memory usage in MB per pod
- Detects continuously increasing trend (leak pattern)
- Triggers alert if memory > 500MB or leak suspected

**Dependency Mapper**
- Loads static pod relationship graph
- Computes blast radius for any faulty pod
- Example: mysql fault → affects backend → affects frontend

### Step 3 — Orchestrator Reasoning
The Orchestrator combines all agent outputs:
f cpu_alert AND memory_alert on same pod:
root_cause = "Pod Overload"
severity   = "CRITICAL"
elif only cpu_alert:
root_cause = "CPU Spike — traffic burst likely"
severity   = "HIGH"
elif only memory_alert:
root_cause = "Memory Leak or Pressure"
severity   = "HIGH"
else:
status = "All pods healthy"
### Step 4 — Recommendation Engine
Based on root cause:
- CPU issue → suggest increasing CPU limit or adding HPA
- Memory issue → suggest increasing memory limit or adding liveness probe
- Both → suggest scaling replicas

### Step 5 — Dashboard Display
All results shown on Streamlit dashboard:
- Live CPU and memory graphs
- Pod dependency visualization
- Active alerts panel
- Recommended fixes
