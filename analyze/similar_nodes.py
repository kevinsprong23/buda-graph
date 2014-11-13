"""
find similar nodes in a graph using jaccard similarity
and cosine similarity

use multiprocessing because n^3 comparison
of each node to every other is very slow

"""

import math
from operator import itemgetter
from functools import partial
from multiprocessing import Pool, cpu_count
import multiprocessing.util as util
from graph_functions import load_adjacency_matrix


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
    return dot(vector_one, vector_two) / max(1, vec_one_norm * vec_two_norm)


def find_missing_edges(node_id, candidate_ids, adj_mat, 
                       num_to_find=10, node_thresh=1):
    """
    find the most similar nodes that don't share an edge with node_id

    candidate_ids is a list of node ids which we want to recommend for

    adj_mat is the adjacency matrix, element ij is the weight between
    nodes with id i+1 and j+1 (because matrices are zero-indexed)

    node_id is a specific node id to find recommendations for
    num_to_find is the number of recommendations to make
    node_thresh filters on node weighted degree - i.e. dont search small nodes

    returns NODE IDs (not matrix indices) and similarity scores
    """
    N = len(adj_mat)
    uid = node_id

    # tuples of uid1,uid2,similarity
    missing_edges = None

    node_one_vec = adj_mat[uid - 1]

    if sum(node_one_vec) >= node_thresh:
        missing_edges = [(uid, uid, float('-inf')) for n in range(num_to_find)]
        for uid2 in candidate_ids:
            # only want unconnected nodes
            if node_one_vec[uid2 - 1] or uid == uid2:
                continue

            node_two_vec = adj_mat[uid2 - 1]

            sim = (jaccard_similarity(node_one_vec, node_two_vec) +
                   cosine_similarity(node_one_vec, node_two_vec))

            if sim >= missing_edges[-1][2]:
                # get rid of the least-similar entry in list
                missing_edges[-1] = (uid, uid2, sim)
                missing_edges.sort(key=itemgetter(2), reverse=True)

    return missing_edges


if __name__ == "__main__":
    node_file_path = '../data/player_graph/nodes.csv'
    edge_file_path = '../data/player_graph/edges.csv'
    candidate_file_path = '../data/player_graph/node_ids_since_2013.txt'

    # adjacency matrix and dict of node id/label
    adj_mat, nodes = load_adjacency_matrix(node_file_path,
                                           edge_file_path)

    # node IDs range from 1 to the number of nodes
    nodes_to_process = []
    with open(candidate_file_path) as cand_file:
        for line in cand_file:
            nodes_to_process.append(int(line))

    # partial function to apply in parallel
    find_edges_partial = partial(find_missing_edges,
                                 candidate_ids=nodes_to_process,
                                 adj_mat=adj_mat,
                                 num_to_find=10, node_thresh=1)

    # parallel generation of results
    util.log_to_stderr(util.SUBDEBUG)
    n_cores = cpu_count()
    chunksize = max(1, len(nodes_to_process) // (2 * (n_cores - 1)))

    pool = Pool(processes=(n_cores - 1))
    similarity_results = pool.imap(find_edges_partial,
                                   nodes_to_process,
                                   chunksize=chunksize)

    # write results to file
    with open('results/similarity_results.csv', 'w') as file_out:
        for result in similarity_results:
            if not result:
                continue
            for (uid, uid2, sim) in result:
                print(nodes[uid], nodes[uid2], round(sim, 2),
                      sep=',', file=file_out)

    pool.close()
    pool.join()



