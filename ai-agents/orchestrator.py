# ai-agents/orchestrator.py

from cpu_agent import run_cpu_agent
from memory_agent import run_memory_agent
from dependency_mapper import run_dependency_mapper, analyze_impact
from recommendation_engine import generate_recommendations
from datetime import datetime

def determine_root_cause(cpu_alerts, memory_alerts):
    """
    Multi-agent reasoning:
    Combines CPU + Memory alerts to find root cause.
    """
    root_causes = []

    cpu_pods = {a["pod"] for a in cpu_alerts}
    memory_pods = {a["pod"] for a in memory_alerts}

    # Both CPU and memory spike on same pod = overload
    overloaded = cpu_pods & memory_pods
    for pod in overloaded:
        root_causes.append({
            "pod": pod,
            "root_cause": "Pod Overload",
            "reason": f"Both CPU spike and memory pressure detected on '{pod}'",
            "severity": "CRITICAL"
        })

    # Only CPU spike
    for pod in cpu_pods - memory_pods:
        root_causes.append({
            "pod": pod,
            "root_cause": "CPU Spike",
            "reason": f"Isolated CPU spike on '{pod}' — possible traffic burst",
            "severity": "HIGH"
        })

    # Only memory issue
    for pod in memory_pods - cpu_pods:
        root_causes.append({
            "pod": pod,
            "root_cause": "Memory Leak / Pressure",
            "reason": f"Memory issue on '{pod}' without CPU spike — possible leak",
            "severity": "HIGH"
        })

    return root_causes

def run_orchestrator():
    print("\n" + "=" * 60)
    print("   PODSENSE — AI ORCHESTRATOR STARTING")
    print("=" * 60)
    print(f"   Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # Step 1: Run all agents
    print("\n[Orchestrator] Step 1: Running CPU Agent...")
    cpu_alerts = run_cpu_agent()

    print("\n[Orchestrator] Step 2: Running Memory Agent...")
    memory_alerts = run_memory_agent()

    print("\n[Orchestrator] Step 3: Running Dependency Mapper...")
    dep_graph = run_dependency_mapper()

    # Step 2: Determine root cause
    print("\n" + "=" * 60)
    print("[Orchestrator] Step 4: Analyzing Root Cause...")
    print("=" * 60)

    root_causes = determine_root_cause(cpu_alerts, memory_alerts)

    if root_causes:
        for rc in root_causes:
            print(f"\n  🔴 Pod      : {rc['pod']}")
            print(f"     Root Cause: {rc['root_cause']}")
            print(f"     Reason    : {rc['reason']}")
            print(f"     Severity  : {rc['severity']}")

            # Blast radius
            impact = analyze_impact(rc["pod"], dep_graph)
            if impact["directly_affected"]:
                print(f"     Blast Radius: {impact['impact_summary']}")
    else:
        print("\n  ✅ No anomalies detected. All pods healthy.")

    # Step 3: Generate recommendations
    print("\n" + "=" * 60)
    print("[Orchestrator] Step 5: Generating Recommendations...")
    print("=" * 60)
    recommendations = generate_recommendations(cpu_alerts, memory_alerts)
    for rec in recommendations:
        print(f"\n  💡 [{rec['pod']}] {rec['recommendation']}")

    # Final summary
    print("\n" + "=" * 60)
    print("[Orchestrator] ANALYSIS COMPLETE")
    print(f"  CPU Alerts    : {len(cpu_alerts)}")
    print(f"  Memory Alerts : {len(memory_alerts)}")
    print(f"  Root Causes   : {len(root_causes)}")
    print(f"  Recommendations: {len(recommendations)}")
    print("=" * 60)

    return {
        "cpu_alerts": cpu_alerts,
        "memory_alerts": memory_alerts,
        "root_causes": root_causes,
        "recommendations": recommendations
    }

if __name__ == "__main__":
    run_orchestrator()
