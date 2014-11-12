"""
find similar players using jaccard similarity
and cosine similarity

use multiprocessing because n^3 comparison
of each player to every other is very slow

"""

import math
from operator import itemgetter
from functools import partial
from multiprocessing import Pool, cpu_count
from graph_functions import build_adjacency_matrix

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


def find_missing_edges(player_id, adj_mat, num_to_find=10, node_thresh=1):
    """
    find the most similar players that haven't played together

    adj_mat is the adjacency matrix, element ij is the weight between
    nodes with id i+1 and j+1 (because matrices are zero-indexed)

    player_id is a specific player id to find recommendations for
    num_to_find is the number of recommendations to make
    node_thresh filters on node weighted degree - i.e. dont search small nodes

    returns NODE IDs (not matrix indices) and similarity scores
    """
    N = len(adj_mat)
    uid = player_id

    # tuples of uid1,uid2,similarity
    missing_edges = [(uid, uid, float('-inf')) for n in range(num_to_find)]

    player_one_vec = adj_mat[uid - 1]

    if sum(player_one_vec) >= node_thresh:
        for uid2 in range(1, N+1):
            # only want unconnected players
            if player_one_vec[uid2 - 1] or uid == uid2:
                continue

            player_two_vec = adj_mat[uid2 - 1]

            sim = (jaccard_similarity(player_one_vec, player_two_vec) +
                   cosine_similarity(player_one_vec, player_two_vec))

            if sim >= missing_edges[-1][2]:
                # get rid of the least-similar entry in list
                missing_edges[-1] = (uid, uid2, sim)
                missing_edges.sort(key=itemgetter(2), reverse=True)

        return missing_edges


def update_results(result, results_list):
    """
    put result in list
    only main process will access this
    """
    results_list.append(result)
    print(len(results_list), flush=True)


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

    players_to_process = [9202, 8473, 4352]

    # multiprocessing to process adjacency matrix
    similarity_results = []  # shared output structure
    update_results_partial = partial(update_results, 
                                     results_list=similarity_results)
    
    pool = Pool(processes=(cpu_count() - 1))
    for uid in players_to_process:
        # call missing edge function asynchronously, and 
        # have main process update results when done
        pool.apply_async(find_missing_edges, args=(uid, adj_mat,),
                         kwds=dict(num_to_find=10, node_thresh=1),
                         callback=update_results_partial)

    pool.close()
    pool.join()

    # write results to file
    with open('results/similarity_results.csv', 'w') as file_out:
        for result in similarity_results:
            if not result:
                continue
            for (uid, uid2, sim) in result:
                print(nodes[uid], nodes[uid2], round(sim, 2),
                      sep=',', file=file_out)



