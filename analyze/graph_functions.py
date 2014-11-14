"""
helper modules to compute and manipulate graph
networks
"""
import numpy as np
from multiprocessing import Array
import ctypes

def read_nodes(node_file_name):
    """ read in a nodes file into dict of id: label """
    nodes = {}
    with open(node_file_name, 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            player_id, label = line.strip().split(',')
            nodes[int(player_id)] = label
    return nodes


def read_edges(edge_file_name):
    """ read in an edges file into dict of (src, tgt) : weight """
    edges = {}
    with open(edge_file_name, 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            src, tgt, lbl, wgt, typ = line.strip().split(',')
            edges[(int(src), int(tgt))] = int(wgt)
    return edges


def find_edge(edges, player_one, player_two):
    """
    find an edge between two players if it exists
    exploits the fact that edges are unique, i.e. will not have
    both A-B and B-A in the edge file, so can return upon first
    match
    """
    if (player_one, player_two) in edges:
        return edges[(player_one, player_two)]
    elif (player_two, player_one) in edges:
        return edges[(player_two, player_one)]

    return 0


def build_adjacency_vector(nodes, edges, player_id):
    """
    build player_id row in the adjacency matrix
    and return it as a list
    """
    num_nodes = len(nodes)
    # build the adjacency matrix entries for player one and player two
    adjacency_vec = []
    for i in range(1, num_nodes):  # since we know uids are 1:num_nodes
        adjacency_vec.append(find_edge(edges, player_id, i))

    return adjacency_vec


def build_adjacency_matrix(nodes, edges):
    """
    build the full adjacency matrix for the undirected graph
    defined by the edge list in edges

    nodes is the node list, and is only used for matrix sizing
    edges has tuple of integer keys for source/target, and weight values
    """
    num_nodes = len(nodes)

    # init the matrix
    adj_mat = np.zeros((num_nodes, num_nodes), dtype=np.int)

    # loop over edges and assign to matrix
    for key, weight in edges.items():
        src, tgt = key
        adj_mat[src-1, tgt-1] = weight
        adj_mat[tgt-1, src-1] = weight

    return adj_mat


def load_adjacency_matrix(node_file_name, edge_file_name):
    """ wrapper for build_adjacency_matrix.  also return nodes """
    # read in nodes as dict of id : name
    nodes = read_nodes(node_file_name)
    # read in edges as dict of (src,tgt),weight
    edges = read_edges(edge_file_name)

    # player graph as adjacency matrix
    adj_mat = build_adjacency_matrix(nodes, edges)
    return adj_mat, nodes


def build_adj_mat_multiproc(nodes, edges):
    """
    like build_adjacency_matrix, but returning a numpy wrapper to a
    multiprocessing.Array
    """
    num_nodes = len(nodes)

    # init the matrix
    adj_mat_base = Array(ctypes.c_int, num_nodes * num_nodes)
    adj_mat = np.ctypeslib.as_array(adj_mat_base.get_obj())
    adj_mat = adj_mat.reshape(num_nodes, num_nodes)

    # loop over edges and assign to matrix
    for key, weight in edges.items():
        src, tgt = key
        adj_mat[src-1, tgt-1] = weight
        adj_mat[tgt-1, src-1] = weight

    return adj_mat_base, adj_mat


def load_adj_mat_multiproc(node_file_name, edge_file_name):
    """ wrapper for build_adj_mat_multiproc.  also return nodes """
    # read in nodes as dict of id : name
    nodes = read_nodes(node_file_name)
    # read in edges as dict of (src,tgt),weight
    edges = read_edges(edge_file_name)

    # player graph as adjacency matrix
    adj_mat_base, adj_mat = build_adj_mat_multiproc(nodes, edges)
    return adj_mat_base, adj_mat, nodes



