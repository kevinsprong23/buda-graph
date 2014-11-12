"""
compute basic statistics about a network:
distributions of node degree, weighted degree,
edge_weight
"""

from collections import defaultdict
from graph_functions import build_adjacency_matrix

def zero():
    """ func for default dict """
    return 0

def calc_node_degrees(adj_mat):
    """ return a list of each node's degree """
    node_deg = [0] * len(adj_mat)
    for i, row in enumerate(adj_mat):
        node_deg[i] = sum((1 for x in row if x > 0))
    return node_deg

def calc_edge_weight_hist(adj_mat):
    """ return a dict of frequency of occurrence of edge weights """
    edge_weight_freq = defaultdict(zero)
    for i, row in enumerate(adj_mat):
        for j, el in enumerate(row):
            if j <= i:
                continue
            edge_weight_freq[el] += 1
    return edge_weight_freq

if __name__ == "__main__":
    pass
