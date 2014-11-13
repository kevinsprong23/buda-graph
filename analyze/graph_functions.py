"""
helper modules to compute and manipulate graph
networks
"""

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

    # init the matrix - this would be easier with numpy
    adj_mat = [0 for n in range(num_nodes)]
    for i in range(num_nodes):
        adj_mat[i] = [0 for n in range(num_nodes)]

    # loop over edges and assign to matrix
    for key, weight in edges.items():
        src, tgt = key
        adj_mat[src-1][tgt-1] = weight
        adj_mat[tgt-1][src-1] = weight

    return adj_mat


def load_adjacency_matrix(node_file_name, edge_file_name):
    """ wrapper for build_adjacency_matrix.  also return nodes """
    # read in nodes as dict of id : name
    nodes = {}
    with open(node_file_name, 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            player_id, label = line.strip().split(',')
            nodes[int(player_id)] = label

    # read in edges as dict of (src,tgt),weight
    edges = {}
    with open(edge_file_name, 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            src, tgt, lbl, wgt, typ = line.strip().split(',')
            edges[(int(src), int(tgt))] = int(wgt)

    # player graph as adjacency matrix
    adj_mat = build_adjacency_matrix(nodes, edges)
    return adj_mat, nodes



