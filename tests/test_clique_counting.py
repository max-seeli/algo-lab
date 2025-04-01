from math import comb

import networkx as nx
import pytest

from algo_lab.clique_counting import chiba_nishizeki


def test_empty_graph():
    G = nx.Graph()
    assert chiba_nishizeki(G, 3) == 0


def test_single_node_graph():
    G = nx.Graph()
    G.add_node(1)
    assert chiba_nishizeki(G, 1) == 1
    assert chiba_nishizeki(G, 2) == 0


def test_single_edge_graph():
    G = nx.Graph()
    G.add_edge(1, 2)
    assert chiba_nishizeki(G, 2) == 1
    assert chiba_nishizeki(G, 3) == 0


def test_triangle_graph():
    G = nx.complete_graph(3)
    assert chiba_nishizeki(G, 3) == 1
    assert chiba_nishizeki(G, 2) == 3


def test_square_no_diagonals():
    G = nx.cycle_graph(4)
    assert chiba_nishizeki(G, 3) == 0
    assert chiba_nishizeki(G, 2) == 4


def test_square_with_diagonal():
    G = nx.cycle_graph(4)
    G.add_edge(0, 2)
    assert chiba_nishizeki(G, 3) == 2  # (0,1,2) and (0,2,3)
    assert chiba_nishizeki(G, 4) == 0


def test_complete_graph_k4():
    G = nx.complete_graph(4)
    assert chiba_nishizeki(G, 4) == 1
    assert chiba_nishizeki(G, 3) == 4
    assert chiba_nishizeki(G, 2) == 6


def test_complete_graph_k5():
    G = nx.complete_graph(5)
    assert chiba_nishizeki(G, 5) == 1
    assert chiba_nishizeki(G, 4) == 5
    assert chiba_nishizeki(G, 3) == 10


def test_disconnected_cliques():
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (1, 3)])  # Triangle clique
    G.add_edges_from([(4, 5), (5, 6), (4, 6)])  # Another triangle clique
    assert chiba_nishizeki(G, 3) == 2
    assert chiba_nishizeki(G, 2) == 6  # each triangle has 3 edges


def test_line_graph():
    G = nx.path_graph(5)
    assert chiba_nishizeki(G, 2) == 4
    assert chiba_nishizeki(G, 3) == 0


def test_star_graph():
    G = nx.star_graph(4)  # node 0 connected to 1,2,3,4
    assert chiba_nishizeki(G, 2) == 4
    assert chiba_nishizeki(G, 3) == 0


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 7])
def test_complete_graph_clique_counts(n):
    G = nx.complete_graph(n)
    for k in range(1, n+1):
        expected_count = comb(n, k)
        assert chiba_nishizeki(G, k) == expected_count


@pytest.mark.parametrize("size", [10, 15])
def test_large_sparse_graph(size):
    G = nx.path_graph(size)
    assert chiba_nishizeki(G, 2) == size - 1
    assert chiba_nishizeki(G, 3) == 0


@pytest.mark.parametrize("size", [8, 12])
def test_cycle_graph_no_cliques(size):
    G = nx.cycle_graph(size)
    assert chiba_nishizeki(G, 3) == 0
    assert chiba_nishizeki(G, 2) == size


@pytest.mark.parametrize("prob, size", [(0.5, 6), (0.7, 8)])
def test_random_graphs(prob, size):
    G = nx.erdos_renyi_graph(size, prob, seed=42)
    # Compare with networkx built-in for verification
    cliques = [clique for clique in nx.enumerate_all_cliques(G)]
    for k in range(1, size+1):
        expected = sum(1 for clique in cliques if len(clique) == k)
        assert chiba_nishizeki(G, k) == expected


@pytest.mark.timeout(5)
def test_large_complete_graph_performance():
    G = nx.complete_graph(15)
    assert chiba_nishizeki(G, 4) == comb(15, 4)
