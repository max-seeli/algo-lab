import networkx as nx

def greedy_peeling(G: nx.Graph) -> nx.DiGraph:
    """
    Takes an undirected graph G and returns a directed graph, where
    edges are oriented by repeatedly selecting the vertex with the lowest degree,
    orienting all its remaining edges outwards, and removing it.
    
    Parameters
    ----------
    G : nx.Graph
        The input undirected graph.

    Returns
    -------
    nx.DiGraph
        The directed graph with greedy-peeling orientation.
    """
    G_copy = G.copy()
    oriented = nx.DiGraph()
    oriented.add_nodes_from(G_copy.nodes())

    while G_copy.nodes:
        min_node = min(G_copy.nodes, key=lambda n: G_copy.degree[n])
        
        # Orient all edges from min_node to its neighbors
        for neighbor in list(G_copy.neighbors(min_node)):
            oriented.add_edge(min_node, neighbor)
            G_copy.remove_edge(min_node, neighbor)
        
        G_copy.remove_node(min_node)

    return oriented
