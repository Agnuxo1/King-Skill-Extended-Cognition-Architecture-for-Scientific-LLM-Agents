---
name: skill-08-networkx
description: >
  Graph analysis, network topology, path finding, centrality, community detection
  using NetworkX. Critical for P2P network analysis in OpenCLAW.
  Triggers: "graph", "network", "topology", "P2P nodes", "centrality",
  "shortest path", "clustering", "community", "DAG", "connectivity".
token_savings: 5/5
dependencies: networkx, matplotlib, scipy
---

## Core patterns

```python
import networkx as nx
import numpy as np

# Build P2P network
G = nx.Graph()
G.add_nodes_from(range(N_nodes))
G.add_edges_from(edges)

# Topology metrics (OpenCLAW context)
metrics = {
    "n_nodes":        G.number_of_nodes(),
    "n_edges":        G.number_of_edges(),
    "avg_degree":     np.mean([d for _,d in G.degree()]),
    "diameter":       nx.diameter(G),
    "clustering":     nx.average_clustering(G),
    "connected":      nx.is_connected(G),
    "betweenness":    nx.betweenness_centrality(G),
    "pagerank":       nx.pagerank(G),
}

# Fault tolerance: remove f nodes, check connectivity
def bft_check(G, f):
    import itertools
    for removed in itertools.combinations(G.nodes(), f):
        H = G.copy()
        H.remove_nodes_from(removed)
        if not nx.is_connected(H):
            return False
    return True  # survives f Byzantine nodes

# DAG operations (for paper dependency graphs)
DAG = nx.DiGraph()
DAG.add_edges_from(dependencies)
order = list(nx.topological_sort(DAG))
```

## P2P consensus simulation

```python
def simulate_consensus(G, initial_states, T=100):
    states = dict(zip(G.nodes(), initial_states))
    for _ in range(T):
        new_states = {}
        for node in G.nodes():
            nbr_states = [states[n] for n in G.neighbors(node)]
            new_states[node] = np.mean(nbr_states + [states[node]])
        states = new_states
    return states  # converged if all ≈ equal
```
