"""
compute basic statistics about a network:
distributions of node degree, weighted degree,
edge_weight
"""

import numpy as np
from graph_functions import load_adjacency_matrix
import aperture as ap
import matplotlib.pyplot as plt
import json

def calc_node_degree(adj_mat):
    """ return a list of each node's degree """
    return np.apply_along_axis(lambda x: len(x[x > 0]), 1, adj_mat)


def calc_weighted_node_degree(adj_mat):
    """ return a list of each node's WEIGHTED degree """
    return np.sum(adj_mat, axis=1)


def get_edge_weight_list(adj_mat):
    """ return a list of the positive edge weights """
    edge_weights = []
    for i, row in enumerate(adj_mat):
        for j, el in enumerate(row):
            if j <= i or not el:
                continue
            edge_weights.append(el)
    return edge_weights


def mean_pos_edge_weight(array):
    """ return mean of the positive elements of array """    
    return np.mean(array[array > 0]) if any(array) else 0


def calc_mean_edge_weight(adj_mat):
    """ return a list of each node's mean positive edge weight """
    return np.apply_along_axis(mean_pos_edge_weight, 1, adj_mat)


if __name__ == "__main__":
    node_file_path = '../data/player_graph/nodes.csv'
    edge_file_path = '../data/player_graph/edges.csv'

    # player graph as adjacency matrix
    adj_mat, nodes = load_adjacency_matrix(node_file_path,
                                           edge_file_path)

    # basic analytics
    node_degrees = calc_node_degree(adj_mat)
    weighted_node_degrees = calc_weighted_node_degree(adj_mat)
    mean_edge_weights = calc_mean_edge_weight(adj_mat)
    edge_weight_list = get_edge_weight_list(adj_mat)

    # get ego results for degrees 1 and 2 (from json'd file):
    ego_json_file = '../app/egos.json'
    first_degree = []
    second_degree = []
    with open(ego_json_file) as file_in:
        ego_str = file_in.readline()
        egos = json.loads(ego_str)
    for player in egos:
        first_degree.append(player['list'][0]['p'])
        second_degree.append(player['list'][1]['p'])

    # plot node degree versus edge weight
    plt.figure()
    plt.plot(weighted_node_degrees, mean_edge_weights, '.', alpha=0.05)
    plt.xlabel('Weighted node degree')
    plt.ylabel('Mean edge weight')
    plt.savefig('results/wgt_node_deg_vs_edge_weight.png')

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

    # plot ego degree results
    plt.figure()
    plt.plot(first_degree, second_degree, '.', alpha=0.2)
    plt.xlabel('% of BUDA directly played with')
    plt.ylabel('% of BUDA at Two Degrees of Separation')
    plt.savefig('results/ego_correlation.png')



