"""
compute basic statistics about a network:
distributions of node degree, weighted degree,
edge_weight
"""

import math
from collections import defaultdict
from graph_functions import build_adjacency_matrix
import aperture as ap
import matplotlib.pyplot as plt

def zero():
    """ func for default dict """
    return 0


def mean(x):
    if not x: 
        return None
    tot = 0
    co = 0
    for val in x:
        tot += val
        co += 1
    if co == 0:
        return 0
    return float(tot) / co

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


def get_edge_weight_list(adj_mat):
    """ return a list of the positive edge weights """
    edge_weights = []
    for i, row in enumerate(adj_mat):
        for j, el in enumerate(row):
            if j <= i or not el:
                continue
            edge_weights.append(el)
    return edge_weights


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

    # read in edges as dict of (src,tgt) : weight
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
    weighted_node_degrees = calc_weighted_node_degree(adj_mat)
    mean_edge_weights = calc_mean_edge_weight(adj_mat)
    edge_weight_list = get_edge_weight_list(adj_mat)

    # plot node degree versus edge weight
    plt.figure()
    plt.plot(node_degrees, mean_edge_weights, '.', alpha=0.05)
    plt.xlabel('Node degree')
    plt.ylabel('Mean edge weight')
    plt.savefig('results/node_deg_vs_edge_weight.png')
    
    # plot node degree hist
    fig = plt.figure()
    plt.hist(node_degrees, bins=range(1000), log=False,
             facecolor=ap.solarized('blue'), edgecolor=ap.solarized('blue'))
    fig.gca().set_xlim([0, 300])
    plt.xlabel('Number of distinct teammates')
    plt.ylabel('Player count')
    plt.savefig('results/node_degree_hist')

    # plot edge weight hist
    fig = plt.figure()
    plt.hist(edge_weight_list, bins=range(100), log=True,
             facecolor=ap.solarized('blue'), edgecolor=ap.solarized('blue'))
    fig.gca().set_xlim([0, 70])
    fig.gca().set_ylim([0.5, 1e6])
    plt.xlabel('Times two given players played together')
    plt.ylabel('Number of occurrences')
    plt.savefig('results/edge_weight_hist')



