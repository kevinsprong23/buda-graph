"""
find similar nodes in a graph using jaccard similarity
and cosine similarity

use multiprocessing because n^3 comparison
of each node to every other is very slow

"""

import math
import numpy as np
import ctypes
from operator import itemgetter
from functools import partial
from multiprocessing import Pool, cpu_count
import multiprocessing.util as util
from graph_functions import load_adj_mat_multiproc

#==============================================================================
# Global variable shenanigans to get numpy to play nice with multiprocessing
node_file_path = '../data/player_graph/nodes.csv'
edge_file_path = '../data/player_graph/edges.csv'
candidate_file_path = '../data/player_graph/node_ids_since_2013.txt'

# adjacency matrix and dict of node id/label
adj_mat_base, adj_mat, nodes = load_adj_mat_multiproc(node_file_path,
                                                      edge_file_path)

# node IDs range from 1 to the number of nodes
nodes_for_comparison = []
with open(candidate_file_path) as cand_file:
    for line in cand_file:
        nodes_for_comparison.append(int(line))
#==============================================================================


def jaccard_similarity(vector_one, vector_two):
    """
    weighted jaccard similarity between two vectors:
    jaccard similarity is len(intersection(x,y))/len(union(x,y))
    for weighted version against indexed vectors it's sum(min) / sum(max)
    """
    vec_min = (min(i, j) for i, j in zip(vector_one, vector_two))
    vec_max = (max(i, j) for i, j in zip(vector_one, vector_two))
    return sum(vec_min) / max(1, sum(vec_max))  # prevent div by zero


def cosine_similarity(vector_one, vector_two):
    """
    cosine similarity between two vectors
    """
    vec_one_norm = max(1, np.linalg.norm(vector_one))
    vec_two_norm = max(1, np.linalg.norm(vector_two))
    return np.dot(vector_one, vector_two) / max(1, vec_one_norm * vec_two_norm)


def find_missing_edges(node_id, candidate_ids=nodes_for_comparison,
                       adj_mat=adj_mat, num_to_find=10, node_thresh=1):
    """
    find the most similar nodes that don't share an edge with node_id

    candidate_ids is a list of node ids which we want to recommend for

    adj_mat is the adjacency matrix as a numpy array,
        element ij is the weight between
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

    node_one_vec = adj_mat[uid - 1, :]

    if sum(node_one_vec) >= node_thresh:
        missing_edges = [(uid, uid, float('-inf')) for n in range(num_to_find)]
        for uid2 in candidate_ids:
            # only want unconnected nodes
            if node_one_vec[uid2 - 1] or uid == uid2:
                continue

            node_two_vec = adj_mat[uid2 - 1, :]

            sim = (jaccard_similarity(node_one_vec, node_two_vec) +
                   cosine_similarity(node_one_vec, node_two_vec))

            if sim >= missing_edges[-1][2]:
                # get rid of the least-similar entry in list
                missing_edges[-1] = (uid, uid2, sim)
                missing_edges.sort(key=itemgetter(2), reverse=True)

    return missing_edges


if __name__ == "__main__":
    # load node id's that we have already processed
    processed_ids = set()
    try:
        with open('results/processed_similarity_ids.txt') as file_in:
            for line in file_in:
                processed_ids.add(int(line))
    except:
        pass

    # process the rest
    nodes_to_process = [x for x in nodes_for_comparison if x not in processed_ids]

    # parallel generation of results
    util.log_to_stderr(util.SUBDEBUG)
    n_cores = cpu_count()
    chunksize = max(1, len(nodes_to_process) // (2 * (n_cores - 1)))

    
    pool = Pool(processes=(n_cores - 1))
    similarity_results = pool.imap(find_missing_edges,
                                   nodes_to_process,
                                   chunksize=chunksize)

    # write results to file
    with open('results/similarity_results.csv', 'a') as file_out, \
         open('results/processed_similarity_ids.txt', 'a') as processed:
        for result in similarity_results:
            if not result:
                continue
            # write the result
            for (uid, uid2, sim) in result:
                print(nodes[uid], nodes[uid2], round(sim, 2),
                      sep=',', file=file_out)
            # log that we have another result
            print(uid, file=processed)

    pool.close()
    pool.join()



