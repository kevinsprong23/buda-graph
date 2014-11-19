"""
find the size of each player's ego network for K <= 6

use multiprocessing for speeeeed

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
nodes_for_comparison = nodes_for_comparison[0:10]
#==============================================================================

def calc_ego_network_sizes(node_id, max_k=6, adj_mat=adj_mat):
    """
    calculate the ego networks up to a given degree for a player
    """
    if max_k < 1:
        return

    ego_results = []

    # do degree 1 manually
    ego_vector = np.zeros(adj_mat.shape[1])  # in case we have down-selected
    ego_vector[adj_mat[node_id - 1] > 0] = 1  # only place we need node id
    ego_results.append((node_id, 1, sum(ego_vector)))  # tuple of results

    # get indices we need to search
    this_ego = np.where(ego_vector > 0)[0]

    # set up processing loop
    next_ego = np.zeros(adj_mat.shape[1])
    for i in range(2, max_k + 1):
        next_ego[:] = 0
        for j in this_ego:
            next_ego[adj_mat[j] > 0] = 1
        ego_vector[next_ego > 0] = 1

        # update ego results and vector for next round
        ego_results.append((node_id, i, sum(ego_vector) + 1))  # include self
        this_ego = np.where(next_ego > 0)[0]

    return ego_results


if __name__ == "__main__":
    # load node id's that we have already processed
    processed_ids = set()
    try:
        with open('results/processed_ego_ids.txt') as file_in:
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
    ego_results = pool.imap(calc_ego_network_sizes,
                                   nodes_to_process,
                                   chunksize=chunksize)

    # write results to file
    sample_size = len(nodes)
    with open('results/ego_results.csv', 'a') as file_out, \
         open('results/processed_ego_ids.txt', 'a') as processed:
        for result in ego_results:
            if not result:
                continue
            # write the result
            for (uid, ego_degree, num_nodes) in result:
                print(uid, ego_degree, round(num_nodes / sample_size, 4),
                      sep=',', file=file_out)
            # log that we have another result
            print(uid, file=processed)

    pool.close()
    pool.join()



