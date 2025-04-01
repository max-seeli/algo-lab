from itertools import combinations

import networkx as nx

import algo_lab.orientation as orientation


def chiba_nishizeki(G: nx.Graph, k: int) -> int:
    """
    Count the number of cliques of size k in the given graph using the 
    Chiba-Nishizeki algorithm.

    Parameters
    ----------
    graph : nx.Graph
        The input graph.
    k : int
        The size of the cliques to count.

    Returns
    -------
    int
        The number of cliques of size k in the graph.
    """
    if k < 1:
        raise ValueError("k must be an integer and at least 1")
    elif k == 1:
        return G.number_of_nodes()
    elif k == 2:
        return G.number_of_edges()


    out_orientation = orientation.greedy_peeling(G)
    cnt = 0

    for (u, v) in G.edges():

        # Ensure u is the node with the lower out-degree
        if out_orientation.has_edge(v, u):
            u, v = v, u

        u_out_neighbors = set(out_orientation.successors(u))
        for w in combinations(u_out_neighbors - set([v]), k-3):

            # Check pairwise adjacency
            if not all(G.has_edge(x, y) for (x, y) in combinations(w, 2)):
                continue
            # Check adjacency with v
            elif not all(G.has_edge(x, v) for x in w):
                continue
            # Increase counter for each common neighbor
            else:
                for x in u_out_neighbors:
                    isAdjacent = True
                    for y in list(w) + [v]:
                        if not G.has_edge(x, y):
                            isAdjacent = False
                            break
                    if isAdjacent:
                        cnt += 1

    return cnt / ((k-1)*(k-2))
