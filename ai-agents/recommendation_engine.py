# ai-agents/recommendation_engine.py

def generate_recommendations(cpu_alerts, memory_alerts):
    """
    Generates actionable fix suggestions based on alerts.
    """
    recommendations = []
    handled_pods = set()

    for alert in cpu_alerts:
        pod = alert["pod"]
        handled_pods.add(pod)
        recommendations.append({
            "pod": pod,
            "issue": "High CPU Usage",
            "recommendation": f"Increase CPU limit for '{pod}' pod in deployment YAML. "
                              f"Consider Horizontal Pod Autoscaler (HPA) if traffic is bursty.",
            "yaml_fix": f"""
resources:
  limits:
    cpu: "500m"       # increase this
  requests:
    cpu: "250m"
"""
        })

    for alert in memory_alerts:
        pod = alert["pod"]
        if pod in handled_pods:
            # Both CPU and memory — add combined recommendation
            recommendations.append({
                "pod": pod,
                "issue": "High CPU + Memory",
                "recommendation": f"'{pod}' is overloaded. Scale horizontally: "
                                  f"increase replicas in deployment. Check for memory leaks in app code.",
                "yaml_fix": f"""
spec:
  replicas: 3    # increase replicas
resources:
  limits:
    memory: "512Mi"   # increase memory limit
"""
            })
        else:
            recommendations.append({
                "pod": pod,
                "issue": "Memory Leak / High Memory",
                "recommendation": f"Increase memory limit for '{pod}'. "
                                  f"Add liveness probe to auto-restart on memory threshold breach.",
                "yaml_fix": f"""
resources:
  limits:
    memory: "512Mi"    # increase this
livenessProbe:
  httpGet:
    path: /health
    port: 8080
  initialDelaySeconds: 30
  periodSeconds: 10
"""
            })

    if not recommendations:
        recommendations.append({
            "pod": "all",
            "issue": "None",
            "recommendation": "All pods are healthy. No action required.",
            "yaml_fix": ""
        })

    return recommendations

def display_recommendations(recommendations):
    print("\n[Recommendation Engine] Suggested Fixes:")
    print("-" * 50)
    for rec in recommendations:
        print(f"\n  Pod    : {rec['pod']}")
        print(f"  Issue  : {rec['issue']}")
        print(f"  Fix    : {rec['recommendation']}")
        if rec["yaml_fix"].strip():
            print(f"  YAML   :{rec['yaml_fix']}")

if __name__ == "__main__":
    # Standalone test
    sample_cpu = [{"pod": "backend", "cpu_usage": 92}]
    sample_mem = [{"pod": "backend", "memory_mb": 620}]
    recs = generate_recommendations(sample_cpu, sample_mem)
    display_recommendations(recs)
