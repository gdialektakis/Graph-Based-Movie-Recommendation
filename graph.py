from typing import Optional, Any
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import UnionColors
import EnergySpreading


# movies.csv
movies_data = pd.read_csv('movies.csv', delimiter=';')
movies_data = movies_data[['movieID', 'title']]

# movie_actors.csv
actors_data = pd.read_csv('movie_actors.csv', delimiter=',')
actors_data = actors_data[['actorName', 'movieID', 'ranking']]

# movie_genres.csv
genre_data = pd.read_csv('movie_genres.csv', delimiter=',')
genre_data = genre_data[['movieID', 'genre']]

genre_data = genre_data.merge(movies_data, on="movieID", how="inner")
actors_data = actors_data.merge(movies_data, on="movieID", how="inner")
genre_data.drop(['movieID'], axis=1, inplace=True)
actors_data.drop(['movieID'], axis=1, inplace=True)

genre_data['edge'] = pd.Series(1, index=genre_data.index)
genre_data.reset_index(drop=True)

# Create a graph
G = nx.Graph()
# Add nodes
G.add_nodes_from(actors_data.actorName, node_type='actor', colors=[])
G.add_nodes_from(movies_data.title, node_type='movie', colors=[])
G.add_nodes_from(genre_data.genre, node_type='genre', colors=[])

for gd in genre_data.values:
    G.add_edge(gd[1], gd[0], relation='movie_genre')

for ac in actors_data.values:
    G.add_edge(ac[2], ac[0], relation='movie_actor')


# Union Colors Algorithms
H = G.copy()
UnionColors.run(H)
M = G.copy()
EnergySpreading.run(M)

#
# color_map = []
# for node in G.nodes(data=True):
#     if 'node_type' in node[1]:
#         n = node[1].get('node_type')
#     else:
#         n = 'red'
#     if n == 'actor':
#         color_map.append('yellow')
#     elif n == 'movie':
#         color_map.append('blue')
#     elif n == 'genre':
#         color_map.append('green')
#     else:
#         color_map.append('red')
#
# nx.draw(G, node_color=color_map, with_labels=True)
# plt.show()
