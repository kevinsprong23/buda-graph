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

    # jsonify
    jsonified = []
    for player in similarity_results:
        j = [{'n': n, 's': s} for n, s in similarity_results[player]]
        jsonified.append({'name': player, 'players': j})
    
    # save
    with open('similarities.json', 'w') as file_out:
        print(json.dumps(jsonified), file=file_out)
