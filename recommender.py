import json

from data.dataset.testData import test_data
from back.engine.CollaborativeFiltering import *
from back.engine import k, CLUSTER_NAME
from data.scrub.dataAPI import getItemName
from config import test
from runCluster import run_cluster

new_user = {}
data = dataAPI.prepareData(trainingData)


def readCluster():
    with open(CLUSTER_NAME, 'rb') as input:
        cluster = pickle.load(input)
        return cluster


def top5Movies(new_user, k, cluster):
    # get the key and ratings of new user
    user_key = list(new_user)[0]
    user_ratings = new_user[user_key]
    n = 5
    # find the closest cluster to the user
    cluster_no = calculateSimilarities(user_ratings, cluster, k)
    user_list = cluster[cluster_no].user_list
    dist = {}
    for i in range(len(user_list)):
        dist[i] = euclideanDistance(user_ratings, data[user_list[i]])
    closer_user = sorted(dist, key=dist.get)
    recommended_movies = []
    for j in range(n):
        for m in range(no_of_items):
            if m > 20:
                rating_of_closer_user = data[closer_user[j]][m]
                if int(rating_of_closer_user) == 5:
                    recommended_movies.append(m + 1)
                    break

    recommended_movies_name = []
    for each_movie_id in recommended_movies:
        recommended_movies_name.append(getItemName(each_movie_id))
    return json.dumps(recommended_movies_name)


def recommend(rate):
    try:
        cluster = readCluster()
    except FileNotFoundError:
        run_cluster(k)
        cluster = readCluster()
    userId = random.randint(101, 999)
    new_user[userId] = rate
    if test == 1:
        recommendation = top5Movies(test_data, k, cluster)
    else:
        recommendation = top5Movies(new_user, k, cluster)

    return recommendation