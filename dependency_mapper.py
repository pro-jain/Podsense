import networkx as nx
import matplotlib.pyplot as plt

dependencies = {
    "frontend": ["backend-api"],
    "backend-api": ["database"],
    "database": []
}

def build_dependency_graph():

    G = nx.DiGraph()

    for pod, deps in dependencies.items():

        for dep in deps:
            G.add_edge(pod, dep)

    return G

def visualize_graph():

    G = build_dependency_graph()

    plt.figure(figsize=(8, 5))

    nx.draw(
        G,
        with_labels=True,
        node_size=3000,
        font_size=10
    )

    plt.title("Pod Dependency Graph")

    plt.show()

def get_impacted_services(pod_name):

    G = build_dependency_graph()

    impacted = list(nx.descendants(G, pod_name))

    return impacted