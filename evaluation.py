import random
from sklearn.metrics import mean_squared_error


def confusion_matrix(y_actual, y_predicted):
    """ This method finds the number of True Positives, False Positives,
    True Negatives and False Negative between the hidden movies
    and those predicted by the recommendation algorithm
    """
    TP = 0
    FP = 0
    TN = 0
    FN = 0

    for i in range(len(y_predicted)):
        if y_actual[i] == y_predicted[i] == 1:
            TP += 1
        if y_predicted[i] == 1 and y_actual[i] != y_predicted[i]:
            FP += 1
        if y_actual[i] == y_predicted[i] == 0:
            TN += 1
        if y_predicted[i] == 0 and y_actual[i] != y_predicted[i]:
            FN += 1

    return TP, FP, TN, FN


def get_metrics(y_actual, y_predicted):
    """ This method computes the evaluation metrics using the above function
        """
    TP, FP, TN, FN = confusion_matrix(y_actual, y_predicted)
    accuracy = float(TP + TN) / float(TP + FP + FN + TN)
    precision = float(TP) / float(TP + FP)
    recall = float(TP) / float(TP + FN)
    print(recall, precision, precision)
    f1_score = 2 * (recall * precision) / (recall + precision)
    rmse = mean_squared_error(y_actual, y_predicted, squared=False)
    rms = mean_squared_error(y_actual, y_predicted)
    return accuracy, precision, recall, f1_score, rmse, rms


def get_labels(G, U, user_id, test_movies, recommendations, category):
    """ This method finds the correct label (0 or 1) of the hidden movies
    and those recommended by the algorithm and stores it into y_actual and y_predicted, respectively.
    """
    y_actual = []
    for movie in test_movies:
        movie_rating = U[user_id][movie]['weight']
        # split the movies into 2 categories, those above 3.5 rating and those below 3.5
        if movie_rating < 3.5:
            y_actual.append(0)
        else:
            y_actual.append(1)

    y_predicted = [0 for y in y_actual]

    for movie in recommendations:
        if movie not in test_movies:
            y_actual_value = 0
            if G.has_edge(movie, category):
                avg_rating = 0
                rating_count = 0
                for u, m in U.edges([movie]):
                    movie_rating = U[u][m]['weight']
                    avg_rating += movie_rating
                    rating_count += 1
                if rating_count > 0:
                    avg_rating = avg_rating / rating_count
                if avg_rating > 3.5:
                    y_actual_value = 1
            y_actual.append(y_actual_value)
            y_predicted.append(1)

    for i in range(len(test_movies)):
        current_test = test_movies[i]
        if current_test in recommendations:
            y_predicted[i] = 1
    return y_actual, y_predicted


def split(U, movie_list, ratio, user_id):
    """ This method selects randomly a number of movies
    to be given as initial nodes to the recommendation algorithms
    """
    random.seed(42)
    split_ratio = ratio
    best_rated_movies = []
    for m in movie_list:
        print(U[user_id][m]['weight'])
        if U[user_id][m]['weight'] > 3.0:
            best_rated_movies.append(m)

    initial_movies = random.sample(best_rated_movies, split_ratio)
    hidden_movies = []
    for m in movie_list:
        if m not in initial_movies:
            hidden_movies.append(m)
    return initial_movies, hidden_movies
