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


def find_missing_edges(nodes, edges, num_to_find=20, node_thresh=1):
    """
    find the most similar players that haven't played together

    nodes is a dictionary of id : name
    edges is a dictionary of source,target : weight by node id
    num_to_find is the number of missing edges to track
    node_thresh filters on node weighted degree - dont search small nodes
    """
    N = len(nodes)
    # tuples of uid1,uid2,similarity
    missing_edges = [(-1, -2, float('-inf')) for n in range(num_to_find)]

    # player uids range from 1 to N
    for uid in range(1, N+1):  # to second-to-last index
        player_one_vec = build_adjacency_vector(nodes, edges, uid)

        if sum(player_one_vec) <= node_thresh:
            continue

        for uid2 in range(uid+1, N+1):  # to last index
            # only want unconnected players
            if (uid, uid2) in edges or (uid2, uid) in edges:
                continue

            player_two_vec = build_adjacency_vector(nodes, edges, uid2)

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

    similar_players = find_missing_edges(nodes, edges)

    for uid, uid2, sim in similar_players:
        print(nodes[uid], nodes[uid2], sim, sep=', ')




