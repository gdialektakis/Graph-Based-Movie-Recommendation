import pandas as pd
import networkx as nx
import UnionColors
import EnergySpreading
import evaluation
import time

#user movie ratings
user_rating_data = pd.read_csv('user_ratings.csv', delimiter=';')
user_rating_data = user_rating_data[['userID', 'movieID', 'rating']]

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

# Add movieTitle on user movie ratings
user_rating_data = user_rating_data.merge(movies_data, on="movieID", how="inner")
user_rating_data.drop(['movieID'], axis=1, inplace=True)

# Create user movie rating graph
U = nx.Graph()
U.add_nodes_from(user_rating_data.userID, node_type='user')
U.add_nodes_from(user_rating_data.title, node_type='movie')
for umr in user_rating_data.values:
    U.add_edge(umr[0], umr[2], relation='rated', weight=umr[1])

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

user_id = 78
genre_to_watch = 'Comedy'
movie_list = []

for u, m in U.edges([user_id]):
    watchable = False
    movie_rating = U[u][m]['weight']
    for m1, g in G.edges([m]):
        if g == genre_to_watch:
            watchable = True
            break
    if watchable:
        movie_list.append(m)

initial_movies, hidden_movies = evaluation.split(movie_list)
# Union Colors Algorithms
H = G.copy()
start_time = time.time()
union_reccomendations = UnionColors.run(H, initial_movies, len(hidden_movies))
finish_time = time.time()

print("\n-----------------Union Colors Algorithm-----------------")
print("Execution time %.2f seconds" % (finish_time-start_time))
print("Movies recommended: %s" % union_reccomendations)


y_actual, y_predicted = evaluation.get_labels(U, user_id, hidden_movies, union_reccomendations)
accuracy, precision, recall, f1_score, rmse, rms = evaluation.get_metrics(y_actual, y_predicted)
print("Accuracy: %.4f " % accuracy)
print("Precision: %.4f " % precision)
print("Recall: %.4f " % recall)
print("F1 Score: %.4f " % f1_score)
print("RMSE: %.4f " % rmse)
print("RMS: %.4f " % rms)


M = G.copy()
start_time = time.time()
energy_recommendations = EnergySpreading.run(M, initial_movies, len(hidden_movies))
finish_time = time.time()

print("\n-----------------Energy Spreading Algorithm-----------------")
print("Execution time %.2f seconds" % (finish_time-start_time))
print("Movies recommended: %s" % energy_recommendations)

energy_recommendations = [rec[0] for rec in energy_recommendations]
y_actual, y_predicted = evaluation.get_labels(U, user_id, hidden_movies, energy_recommendations)
accuracy, precision, recall, f1_score, rmse, rms = evaluation.get_metrics(y_actual, y_predicted)
print("Accuracy: %.4f " % accuracy)
print("Precision: %.4f " % precision)
print("Recall: %.4f " % recall)
print("F1 Score: %.4f " % f1_score)
print("RMSE: %.4f " % rmse)
print("RMS: %.4f " % rms)

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
