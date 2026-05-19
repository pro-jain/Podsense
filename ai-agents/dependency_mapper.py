# ai-agents/dependency_mapper.py

# Pod dependency graph — matches your actual K8s setup
DEPENDENCY_GRAPH = {
    "frontend": ["backend"],
    "backend": ["mysql"],
    "mysql": []
}

def get_dependency_chain(start_pod, graph=DEPENDENCY_GRAPH):
    """
    Returns full dependency chain from a starting pod.
    Example: frontend → backend → mysql
    """
    chain = [start_pod]
    current = start_pod

    while graph.get(current):
        next_pod = graph[current][0]
        chain.append(next_pod)
        current = next_pod

    return chain

def get_upstream_pods(target_pod, graph=DEPENDENCY_GRAPH):
    """
    Returns all pods that depend on the given pod.
    Useful for blast radius analysis.
    """
    upstream = []
    for pod, deps in graph.items():
        if target_pod in deps:
            upstream.append(pod)
    return upstream

def get_downstream_pods(target_pod, graph=DEPENDENCY_GRAPH):
    """
    Returns all pods that the given pod depends on.
    """
    return graph.get(target_pod, [])

def analyze_impact(faulty_pod, graph=DEPENDENCY_GRAPH):
    """
    Given a faulty pod, calculates blast radius.
    Which pods will be affected upstream?
    """
    affected = get_upstream_pods(faulty_pod, graph)
    return {
        "faulty_pod": faulty_pod,
        "directly_affected": affected,
        "downstream_of_faulty": get_downstream_pods(faulty_pod, graph),
        "impact_summary": f"If '{faulty_pod}' fails → affects: {affected if affected else 'No upstream pods'}"
    }

def display_dependency_map(graph=DEPENDENCY_GRAPH):
    print("\n[Dependency Mapper] Pod Dependency Map:")
    print("-" * 40)
    for pod, deps in graph.items():
        if deps:
            print(f"  {pod}  →  {' → '.join(deps)}")
        else:
            print(f"  {pod}  →  (no dependencies)")
    print("-" * 40)

def run_dependency_mapper():
    print("=" * 50)
    print("[Dependency Mapper] Mapping pod relationships...")
    print("=" * 50)

    display_dependency_map()

    # Show full chain from frontend
    chain = get_dependency_chain("frontend")
    print(f"\n[Dependency Mapper] Full Chain: {' → '.join(chain)}")

    # Impact analysis for each pod
    print("\n[Dependency Mapper] Blast Radius Analysis:")
    for pod in DEPENDENCY_GRAPH:
        impact = analyze_impact(pod)
        print(f"  {impact['impact_summary']}")

    return DEPENDENCY_GRAPH

if __name__ == "__main__":
    run_dependency_mapper()
