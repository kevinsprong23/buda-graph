"""
print the N most similar players from the
similarity results file
"""

from operator import itemgetter

if __name__ == "__main__":
    num_to_print = 20

    results_file = '../analyze/results/similarity_results.csv'
    similarity_dict = {}
    with open(results_file) as file_in:
        for line in file_in:
            player, player2, sim = line.strip().split(',')
            if ((player, player2) not in similarity_dict and
                (player2, player) not in similarity_dict):
                similarity_dict[player, player2] = sim

    sorted_sim = sorted(similarity_dict.items(),
                        key=itemgetter(1),
                        reverse=True)
    for i in range(num_to_print):
        print(sorted_sim[i][0][0], sorted_sim[i][0][1],
              sorted_sim[i][1], sep=',')

