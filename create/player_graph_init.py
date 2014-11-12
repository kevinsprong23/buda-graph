"""
from player_data.tsv, get the list
of distinct player names
"""

import re
import unicodedata

def format_name(name):
    """
    turn
    Sprong, Kevin
    into
    Kevin Sprong
    also strip out any crazy unicode stuff
    """
    name_match = re.search(r"(.*),\s(.*)", name)
    if name_match:
        name = name_match.group(2) + " " + name_match.group(1)
        normed_name = (unicodedata.normalize('NFKD', name)
                   .encode('ascii', 'ignore')
                   .decode('utf-8'))
        # now get rid of commas
        return re.sub(r",", "", normed_name)
    else:
        print(name)
        quit()


def parse_line(line):
    """
    return player, team, league, season
    from a line of the player_data file
    """
    return line.strip().split('\t')


def process_team(this_team, nodes, file_obj_out):
    """
    write all of the combinations of players in
    <this_team> as graph edges to <file_obj_out>,
    using the player_ids in <nodes>
    """
    for i, player_one in enumerate(this_team):
        for j, player_two in enumerate(this_team):
            if j > i and nodes[player_one] != nodes[player_two]:
                # write the source id and target id to file
                print(nodes[player_one], nodes[player_two],
                      player_one + " - " + player_two,
                      sep=',', file=file_obj_out)


def extract_nodes(file_name, file_name_out):
    """
    get a dictionary of player names mapped to
    unique ids
    """
    with open(file_name, 'r') as file_in:
        nodes = {}  # dict of player and unique id
        uid = 1
        for line in file_in:
            fields = parse_line(line)
            player = format_name(fields[0])
            if player not in nodes:
                nodes[player] = uid
                uid += 1

    with open(file_name_out, 'w') as file_out:
        print('id,label', file=file_out)
        for player in nodes:
            print(nodes[player], player, sep=',', file=file_out)

    return nodes


def extract_edges(file_name, file_name_out, nodes):
    """
    with a node list, extract edges of the form
    source_id, target_id
    """
    with open(file_name, 'r') as file_in, open(file_name_out, 'w') as file_out:
        print('source,target,label', file=file_out)

        # init the previous entry for comparison
        last_player, last_team, last_league, last_season = (None, None,
                                                            None, None)
        this_team = []
        for line in file_in:
            player, team, league, season = parse_line(line)
            player = format_name(player)
            if last_player is None or (team == last_team and
                league == last_league and season == last_season):
                this_team.append(player)
            else:  # new player
                # process existing team
                process_team(this_team, nodes, file_out)

                # reset and add first player of new team
                this_team = []
                this_team.append(player)

            last_player, last_team, last_league, last_season = (player,
                team, league, season)

        # there is one last team to process
        process_team(this_team, nodes, file_out)


if __name__ == '__main__':
    # get nodes, then edges for player-centric graph
    file_name_in = 'data/roster_data.tsv'
    node_file_out = 'data/player_graph/nodes.csv'
    edge_file_out = 'data/player_graph/raw_edges.csv'

    nodes = extract_nodes(file_name_in, node_file_out)
    extract_edges(file_name_in, edge_file_out, nodes)




