"""
find node ids of players that have recently played
"""

from parse_tools import parse_line, format_name

def find_recent_ids(nodes, year_thresh, roster_file_name):
    """
    loop through roster file and check players
    against thresh. return ids of new players from nodes
    """
    recent_players = set()

    with open(roster_file_name) as file_in:
        for line in file_in:
            player, _, _, year = parse_line(line)

            if int(year) >= year_thresh:
                recent_players.add(format_name(player))

    recent_ids = []
    for node_id, name in nodes.items():
        if name in recent_players:
            recent_ids.append(node_id)
    return recent_ids

if __name__ == "__main__":
    node_file_name = '../data/player_graph/nodes.csv'
    roster_file_name = '../data/roster_data.tsv'

    year_thresh = 2013

    output_file_name = '../data/player_graph/node_ids_since_'
    output_file_name += str(year_thresh)
    output_file_name += '.txt'

    # read nodes
    nodes = {}
    with open(node_file_name, 'r') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            player_id, label = line.strip().split(',')
            nodes[int(player_id)] = label

    recent_ids = find_recent_ids(nodes, int(year_thresh),
                                 roster_file_name)

    with open(output_file_name, 'w') as file_out:
        for rid in recent_ids:
            print(rid, file=file_out)
