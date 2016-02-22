Analysis of the BUDA Social Graph
=================================

Repository for analysis of [BUDA](http://buda.org) players when considered as a social graph

Read more [on my blog](http://kevinsprong.com/posts/2014/11/21/buda-social-graph/). 

A note: I used python 3.3 for this, and made no effort towards python 2.x compatibility. Sorry.

Dependencies: 

* numpy
* matplotlib 

STEPS TO RUN
============

###Create

* scrape.py: this function gets raw roster data from buda.org by following the links in data/links.txt. In lieu of using a headless browser, links.txt was generated by hand
* player_graph_init.py: this combs the data/roster_data.tsv file and creates a list of nodes, one per player. It also creates one edge for each pair of players that played on the same team
* combine_raw_edges.py: this combines the edges from player_graph_init into a set of weighted edges (so twenty different A,B edges throughout the seasons become (A,B,20))
* find_recent_players.py: find nodes that have appeared in a league *recently*, to filter down the number of computations we have to do in similar_players.py

###Analyze

* network_statistics.py: basic statistics about the network (node degree, edge weight)
* similar_players.py: this is essentially a recommender system for each player: this searches all other players and find the list of N players most 'similar' to that player, and writes out the concatenation of each player's list to a file. 'similarity' here is the sum of [weighted jaccard similarity](http://static.googleusercontent.com/media/research.google.com/en/us/pubs/archive/36928.pdf) and [cosine similarity](http://en.wikipedia.org/wiki/Cosine_similarity).
* ego_networks.py: this computes the % of BUDA covered for each recent player as a function of the degrees of separation K.

###App

a quick Angular-based search capability embedded in the blog post. The version here will run standalone in a web container


###Data

this directory contains all of the outputs of the scripts above

the node list and adjacency list in player_graph/ are tailored for import into [Gephi](http://gephi.github.io/).
