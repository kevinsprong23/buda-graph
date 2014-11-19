"""
turn results into json format for webapp
"""

import json

if __name__ == "__main__":
    # read into dict
    similarity_results = {}
    with open('../analyze/results/similarity_results.csv') as file_in:
        for line in file_in:
            player, player2, sim = line.strip().split(',')
            if player not in similarity_results:
                similarity_results[player] = []
            similarity_results[player].append((player2, float(sim)))

    ego_results = {}
    with open('../analyze/results/ego_results.csv') as file_in:
        for line in file_in:
            pid, K, pct = line.strip().split(',')
            if pid not in ego_results:
                ego_results[pid] = []
            ego_results[pid].append((K, float(pct)))

    # nodes
    nodes = {}
    with open('../data/player_graph/nodes.csv') as file_in:
        next(file_in)  # skip header row
        for line in file_in:
            player_id, label = line.strip().split(',')
            nodes[label] = int(player_id)

    # jsonify
    jsonified_results = []
    jsonified_nodes = []
    for player in similarity_results:
        j = [{'n': nodes[n], 's': s} for n, s in similarity_results[player]]
        pid = nodes[player]
        jsonified_results.append({'id': pid, 'list': j})
        jsonified_nodes.append({'id': pid, 'label': player})

    # ego network results have id directly encoded instead of name
    jsonified_ego = []
    for pid in ego_results:
        j = [{'k': K, 'p': round(100 * pct, 2)} for K, pct in ego_results[pid]]
        jsonified_ego.append({'id': pid, 'list': j})

    # save
    with open('similarities.json', 'w') as file_out:
        print(json.dumps(jsonified_results), file=file_out)

    with open('nodes.json', 'w') as file_out:
        print(json.dumps(jsonified_nodes), file=file_out)

    with open('egos.json', 'w') as file_out:
        print(json.dumps(jsonified_ego), file=file_out)
