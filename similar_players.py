"""
find similar players using jaccard similarity
and cosine similarity

the 12k by 12k adjacency matrix does not fit
in memory on my machine, so I am doing it player by player.
This leads to a LOT of wasted edge list traversals.
Should optimize this by figuring out the largest
subgraph that can fit in memory
"""

import math
from operator import itemgetter

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


def jaccard_similarity(vector_one, vector_two):
    """
    weighted jaccard similarity between two vectors:
    jaccard similarity is len(intersection(x,y))/len(union(x,y))
    for weighted version against indexed vectors it's sum(min) / sum(max)
    """
    vec_min = (min(i, j) for i, j in zip(vector_one, vector_two))
    vec_max = (max(i, j) for i, j in zip(vector_one, vector_two))
    return sum(vec_min) / max(1, sum(vec_max))  # prevent div by zero


def norm(vec):
    """ L2 norm """
    return math.sqrt(sum((x ** 2 for x in vec)))


def dot(vec_one, vec_two):
    """ reimplement to avoid numpy dependency """
    return sum((a * b for a, b in zip(vec_one, vec_two)))


def cosine_similarity(vector_one, vector_two):
    """
    cosine similarity between two vectors
    """
    vec_one_norm = max(1, norm(vector_one))
    vec_two_norm = max(1, norm(vector_two))
    return dot(vector_one, vector_two) / (vec_one_norm * vec_two_norm)


def find_missing_edges(adj_mat, player_id=None, num_to_find=50, node_thresh=1):
    """
    find the most similar players that haven't played together

    adj_mat is the adjacency matrix, element ij is the weight between
    nodes with id i+1 and j+1 (because matrices are zero-indexed)

    player_id is a specific player id to limit the recommendations to
    num_to_find is the number of missing edges to track
    node_thresh filters on node weighted degree - dont search small nodes

    returns NODE IDs (not matrix indices) and similarity scores
    """
    # tuples of uid1,uid2,similarity
    missing_edges = [(-1, -2, float('-inf')) for n in range(num_to_find)]

    N = len(nodes)
    if player_id:
        ids_to_search = range(player_id, player_id+1)
    else:
        ids_to_search = range(1, N+1)

    # player uids range from 1 to N
    for uid in ids_to_search:  # to second-to-last index
        print("Searching player {0}".format(uid), flush=True)

        player_one_vec = adj_mat[uid - 1] 

        if sum(player_one_vec) <= node_thresh:
            continue

        ids_to_compare = range(1, N+1) if player_id else range(uid+1, N+1)

        for uid2 in ids_to_compare:  # to last index
            # only want unconnected players
            if adj_mat[uid - 1][uid2 - 1] or uid == uid2:
                continue

            player_two_vec = adj_mat[uid2 - 1]

            if sum(player_two_vec) <= node_thresh:
                continue

            sim = (jaccard_similarity(player_one_vec, player_two_vec) +
                   cosine_similarity(player_one_vec, player_two_vec))

            if sim >= missing_edges[-1][2]:
                # get rid of the least-similar entry in list
                missing_edges[-1] = (uid, uid2, sim)
                missing_edges.sort(key=itemgetter(2), reverse=True)

    return missing_edges


if __name__ == "__main__":
    # read in nodes as dict of id : name
    nodes = {}
    with open('data/player_graph/nodes.csv', 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            player_id, label = line.strip().split(',')
            nodes[int(player_id)] = label

    # read in edges as dict of (src,tgt),weight
    edges = {}
    with open('data/player_graph/edges.csv', 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            src, tgt, lbl, wgt, typ = line.strip().split(',')
            edges[(int(src), int(tgt))] = int(wgt)

    adj_mat = build_adjacency_matrix(nodes, edges)
    similar_players = find_missing_edges(adj_mat, node_thresh=50)

    for uid, uid2, sim in similar_players:
        print(nodes[uid], nodes[uid2], sim, sep=', ')



