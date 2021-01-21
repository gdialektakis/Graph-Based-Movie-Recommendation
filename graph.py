import pandas as pd
import networkx as nx
import UnionColors
import EnergySpreading
import evaluation
import time


def graph(index, user_id, category, ratio):

    # user movie ratings
    user_rating_data = pd.read_csv('user_ratings.csv', delimiter=';')
    user_rating_data = user_rating_data[['userID', 'movieID', 'rating']]

    # movies
    movies_data = pd.read_csv('movies.csv', delimiter=';')
    movies_data = movies_data[['movieID', 'title']]

    # movie_actors
    actors_data = pd.read_csv('movie_actors.csv', delimiter=',')
    actors_data = actors_data[['actorName', 'movieID', 'ranking']]

    # movie_genres
    genre_data = pd.read_csv('movie_genres.csv', delimiter=',')
    genre_data = genre_data[['movieID', 'genre']]

    genre_data = genre_data.merge(movies_data, on="movieID", how="inner")
    actors_data = actors_data.merge(movies_data, on="movieID", how="inner")
    # drop movieID from genre and actors as we won't need it
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
    # Add actor, movie and genre nodes
    G.add_nodes_from(actors_data.actorName, node_type='actor', colors=[])
    G.add_nodes_from(movies_data.title, node_type='movie', colors=[])
    G.add_nodes_from(genre_data.genre, node_type='genre', colors=[])

    # add edges
    for gd in genre_data.values:
        G.add_edge(gd[1], gd[0], relation='movie_genre')

    for ac in actors_data.values:
        G.add_edge(ac[2], ac[0], relation='movie_actor')

    user_id = user_id
    genre_to_watch = category

    # Get statistics about the data
    evaluation.get_statistics(nx, G, U)
    movie_list = []

    for u, m in U.edges([user_id]):
        watchable = False
        rating = U[u][m]['weight']
        for m1, g in G.edges([m]):
            if g == genre_to_watch and rating > 3:
                watchable = True
                break
        if watchable:
            movie_list.append(m)
    # get the initial movies and the hidden ones
    initial_movies, hidden_movies = evaluation.split(U, movie_list, ratio, user_id)

    if index == 0:
        # Union Colors Algorithms
        H = G.copy()
        start_time = time.time()
        union_recommendations = UnionColors.run(H, initial_movies, len(hidden_movies))
        finish_time = time.time()

        print("\n-----------------Union Colors Algorithm-----------------")
        print("Execution time %.2f seconds" % (finish_time-start_time))
        print("Movies recommended: %s" % union_recommendations)


        y_actual, y_predicted = evaluation.get_labels(G, U, user_id, hidden_movies, union_recommendations, category)
        accuracy, precision, recall, f1_score, rmse, rms = evaluation.get_metrics(y_actual, y_predicted)
        print("Accuracy: %.4f " % accuracy)
        print("Precision: %.4f " % precision)
        print("Recall: %.4f " % recall)
        print("F1 Score: %.4f " % f1_score)
        print("RMSE: %.4f " % rmse)
        print("RMS: %.4f " % rms)

        results = {
            'time':  (finish_time-start_time),
            'movies': union_recommendations,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'rmse': rmse,
            'rms': rms
        }
        return results

    else:

        M = G.copy()
        start_time = time.time()
        energy_recommendations = EnergySpreading.run(M, initial_movies, len(hidden_movies))
        finish_time = time.time()

        print("\n-----------------Energy Spreading Algorithm-----------------")
        print("Execution time %.2f seconds" % (finish_time-start_time))
        print("Movies recommended: %s" % energy_recommendations)

        # obtain only the movie without its energy
        energy_recommendations = [rec[0] for rec in energy_recommendations]

        y_actual, y_predicted = evaluation.get_labels(G, U, user_id, hidden_movies, energy_recommendations, category)
        accuracy, precision, recall, f1_score, rmse, rms = evaluation.get_metrics(y_actual, y_predicted)
        print("Accuracy: %.4f " % accuracy)
        print("Precision: %.4f " % precision)
        print("Recall: %.4f " % recall)
        print("F1 Score: %.4f " % f1_score)
        print("RMSE: %.4f " % rmse)
        print("RMS: %.4f " % rms)

        results = {
            'time':  (finish_time-start_time),
            'movies': energy_recommendations,
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score,
            'rmse': rmse,
            'rms': rms
        }
        return results
