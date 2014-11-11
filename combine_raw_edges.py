"""
turn raw edges into weighted graph edges

NOTE: this exploits the fact that raw roster data is
in alphabetical order by name. So connections between
A and B should always show up as A-B
"""

from collections import defaultdict

def one():
    """ function for defaultdict """
    return 1

def combine_raw_edges(file_name, file_name_out):
    """
    find raw edges (one per team/league)
    and combine by number of occurences overall
    """
    with open(file_name, 'r') as file_in:
        next(file_in)  # skip header row
        edges = defaultdict(one)
        for line in file_in:
            edges[line.strip()] += 1

    with open(file_name_out, 'w') as file_out:
        print('source,target,label,weight,type', file=file_out)
        for edge in edges:
            print(edge, edges[edge], 'undirected',
                  sep=',', file=file_out)

if __name__ == '__main__':
    file_name_in = 'data/player_graph/raw_edges.csv'
    file_name_out = 'data/player_graph/edges.csv'

    combine_raw_edges(file_name_in, file_name_out)
