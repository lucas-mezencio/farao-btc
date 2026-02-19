import networkx as nx
import matplotlib.pyplot as plt


def enshort_addr(addr: str) -> str:
    if len(addr) > 10:
        return f"{addr[:4]}...{addr[-4:]}"
    return addr


def view_cluster(cluster: list, target_addr: str):
    G = nx.Graph()

    short_target_addr = enshort_addr(target_addr)
    G.add_node(short_target_addr, color="red", size=800)

    for i, cluster in enumerate(cluster):
        cluster_name = f"C[{i}]"

        G.add_node(cluster_name, color="blue", size=500)
        G.add_edge(cluster_name, short_target_addr)

        for addr in cluster:
            short_addr = enshort_addr(addr)
            G.add_node(short_addr, color="green", size=100)
            G.add_edge(short_addr, cluster_name)

    plt.figure(figsize=(30, 30))
    pos = nx.spring_layout(G, k=0.5, iterations=100)

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color=[G.nodes[node]["color"] for node in G.nodes],
        node_size=[G.nodes[node]["size"] for node in G.nodes],
        font_size=8,
        font_color="dimgray",
        font_weight="bold",
        font_family="monospace",
        edge_color="lightgray",
    )

    plt.title("Analise Forense - Faraó do Bitcoin")

    plt.savefig("cluster.png", format="PNG", dpi=300, bbox_inches="tight")
