import random


def confusion_matrix(y_actual, y_predicted):
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
    TP, FP, TN, FN = confusion_matrix(y_actual, y_predicted)
    accuracy = (TP + TN) / (TP + FP + FN + TN)
    precision = TP / (TP + FP)
    recall = TP / (TP + FN)
    f1_score = 2 * (recall * precision) / (recall + precision)
    return accuracy, precision, recall, f1_score


def get_labels(U, user_id, test_movies, recommendations):
    y_actual = []
    for movie in test_movies:
        movie_rating = U[user_id][movie]['weight']
        if movie_rating < 4.5:
            y_actual.append(0)
        else:
            y_actual.append(1)

    y_predicted = [0 for y in y_actual]

    for movie in recommendations:
        if movie not in test_movies:
            y_actual.append(0)
            y_predicted.append(1)

    for i in range(len(test_movies)):
        current_test = test_movies[i]
        if current_test in recommendations:
            y_predicted[i] = 1

    return y_actual, y_predicted


def split(movie_list):
    random.seed(42)
    # split_ratio = min(int(len(movie_list) * 0.99), len(movie_list) - 2)
    split_ratio = 5
    initial_movies = random.sample(movie_list, split_ratio)
    hidden_movies = []
    for m in movie_list:
        if m not in initial_movies:
            hidden_movies.append(m)
    return initial_movies, hidden_movies
