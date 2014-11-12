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

def calc_node_degree(adj_mat):
    """ return a list of each node's degree """
    node_deg = [0] * len(adj_mat)
    for i, row in enumerate(adj_mat):
        node_deg[i] = sum((1 for x in row if x > 0))
    return node_deg


def calc_weighted_node_degree(adj_mat):
    """ return a list of each node's WEIGHTED degree """
    w_node_deg = [0] * len(adj_mat)
    for i, row in enumerate(adj_mat):
        w_node_deg[i] = sum((x for x in row if x > 0))
    return w_node_deg


def calc_edge_weight_hist(adj_mat):
    """ return a dict of frequency of occurrence of edge weights """
    edge_weight_freq = defaultdict(zero)
    for i, row in enumerate(adj_mat):
        for j, el in enumerate(row):
            if j <= i:
                continue
            edge_weight_freq[el] += 1
    return edge_weight_freq


def calc_mean_edge_weight(adj_mat):
     """ return a list of each node's mean positive edge weight """
    mean_weight = [0] * len(adj_mat)
    for i, row in enumerate(adj_mat):
        mean_weight[i] = mean((x for x in row if x > 0))
    return mean_weight


if __name__ == "__main__":
    # read in nodes as dict of id : name
    nodes = {}
    with open('../data/player_graph/nodes.csv', 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            player_id, label = line.strip().split(',')
            nodes[int(player_id)] = label

    # read in edges as dict of (src,tgt),weight
    edges = {}
    with open('../data/player_graph/edges.csv', 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            src, tgt, lbl, wgt, typ = line.strip().split(',')
            edges[(int(src), int(tgt))] = int(wgt)

    # player graph as adjacency matrix
    adj_mat = build_adjacency_matrix(nodes, edges)

    # basic analytics
    node_degrees = calc_node_degree(adj_mat)
    weighted_node_degree = calc_weighted_node_degree(adj_mat)
    calc_mean_edge_weight(adj_mat)
    edge_weights_frequencies = calc_edge_weight_hist(adj_mat)



