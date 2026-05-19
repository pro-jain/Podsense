# PodSense — System Architecture

## Overview
PodSense is an intelligent Kubernetes observability platform that combines
real-time monitoring with AI-powered root cause analysis.

---

## High-Level Architecture
---

│                  Kubernetes Cluster                     │
│                                                         │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│   │ Frontend │───▶│ Backend  │───▶│  MySQL   │         │
│   │   Pod    │    │   Pod    │    │   Pod    │          │
│   └──────────┘    └──────────┘    └──────────┘          │
│         │               │               │               │
│         └───────────────┴───────────────┘               │
│                         │                               │
│                  ┌──────▼──────┐                        │
│                  │  Prometheus │                        │
│                  │  (Metrics)  │                        │
│                  └──────┬──────┘                        │
└─────────────────────────┼───────────────────────────────┘
│
┌────────────▼────────────┐
│     AI Agent Layer      │
│                         │
│  ┌─────────────────┐    │
│  │   CPU Agent     │    │
│  ├─────────────────┤    │
│  │  Memory Agent   │    │
│  ├─────────────────┤    │
│  │ Dependency      │    │
│  │ Mapper          │    │
│  └────────┬────────┘    │
│           │             │
│  ┌────────▼────────┐    │
│  │  Orchestrator   │    │
│  │ (Root Cause AI) │    │
│  └────────┬────────┘    │
│           │             │
│  ┌────────▼────────┐    │
│  │ Recommendation  │    │
│  │    Engine       │    │
│  └─────────────────┘    │
└────────────┬────────────┘
│
┌────────────▼────────────┐
│      Dashboard          │
│  (Streamlit / React)    │
│  - CPU Graph            │
│  - Memory Graph         │
│  - Dependency Map       │
│  - Alerts Panel         │
└─────────────────────────┘

## Component Details

### 1. Kubernetes Layer (Team Member 1)
| File | Purpose |
|------|---------|
| frontend.yaml | Frontend pod deployment |
| backend.yaml | Backend pod deployment |
| mysql.yaml | MySQL deployment |
| *-service.yaml | Service exposure |
| pvc.yaml | Persistent volume claim |

### 2. Monitoring Layer
| File | Purpose |
|------|---------|
| prometheus-config.yaml | Scrape pod metrics |
| grafana-dashboard.json | Visual dashboard config |
| metrics-queries.md | PromQL reference queries |

### 3. AI Agent Layer
| Agent | Responsibility |
|-------|---------------|
| cpu_agent.py | Detect CPU spikes (threshold > 80%) |
| memory_agent.py | Detect memory leaks and pressure |
| dependency_mapper.py | Map pod relationships and blast radius |
| orchestrator.py | Combine agent outputs, find root cause |
| recommendation_engine.py | Generate actionable fix suggestions |

### 4. Data Flow
Pod Metrics
→ Prometheus scrapes every 15s
→ AI Agents pull metrics
→ CPU Agent detects spikes
→ Memory Agent detects leaks
→ Dependency Mapper finds blast radius
→ Orchestrator correlates findings
→ Recommendation Engine suggests fixes
→ Dashboard displays everything
