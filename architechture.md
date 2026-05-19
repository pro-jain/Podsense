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
│                        │
└────────────┬────────────┘
│
┌────────────▼────────────┐
│ Graphana Dashboard      │
│    │
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




### 3. Data Flow
Pod Metrics
→ Prometheus scrapes every 15s
→ AI Agents pull metrics
→ CPU Agent detects spikes
→ Memory Agent detects leaks
→ Dashboard displays everything
