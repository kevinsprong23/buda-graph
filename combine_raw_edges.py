"""
turn raw edges into weighted graph edges
"""

from collections import defaultdict

def one():
    """ function for defaultdict """
    return 1

def combine_raw_edges(file_name, file_name_out):
    with open(file_name, 'r') as file_in:
        edges = defaultdict(one)
        for line in file_in:
            edges[line.strip()] += 1
    
    with open(file_name_out, 'w') as file_out:
        print('source,target,weight,type', file=file_out)
        for edge in edges:
            print(edge, edges[edge], 'undirected',
                  sep=',', file=file_out)

if __name__ == '__main__':
    file_name_in = 'data/player_graph/raw_edges.csv'
    file_name_out = 'data/player_graph/edges.csv'

    combine_raw_edges(file_name_in, file_name_out)
