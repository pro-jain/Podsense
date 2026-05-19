# PromQL Metrics Queries

## CPU Usage
```promql
sum(rate(container_cpu_usage_seconds_total[1m])) by (pod)
```

## Memory Usage
```promql
container_memory_usage_bytes{namespace="default"}
```

## Network Receive Rate
```promql
rate(container_network_receive_bytes_total[1m])
```

## Pod Restart Count
```promql
kube_pod_container_status_restarts_total
```

## CPU Throttling
```promql
rate(container_cpu_throttled_seconds_total[5m])
```
