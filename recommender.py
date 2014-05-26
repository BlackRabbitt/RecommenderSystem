from engine.CollaborativeFiltering import *
from engine import k
from scrub.dataAPI import getItemName


new_user = {}
data = dataAPI.prepareData(trainingData)
def readCluster():
    with open('cluster.pkl', 'rb') as input:
        cluster = pickle.load(input)
        return cluster


def top5Movies(new_user, k, cluster):
    # get the key and ratings of new user
    user_key = list(new_user)[0]
    user_ratings = new_user[user_key]
    # find the closest cluster to the user
    cluster_no = calculateSimilarities(user_ratings, cluster, k)
    user_list = cluster[cluster_no].user_list
    dist = {}
    for i in range(len(user_list)):
        dist[i] = euclideanDistance(user_ratings, data[cluster[cluster_no].user_list[i]])
    closer_user = sorted(dist, key=dist.get)
    recommended_movies = []
    for j in range(5):
        rating_of_closer_user = data[cluster[cluster_no].user_list[closer_user[j]]]
        print(data[cluster[cluster_no].user_list[6]])
        print(closer_user[j], rating_of_closer_user)
        for i in range(len(rating_of_closer_user)):
            if int(rating_of_closer_user[i]) == 5:
                recommended_movies.append(i + 1)
                break
    recommended_movies_name = []
    for each_movie_id in recommended_movies:
        recommended_movies_name.append(getItemName(each_movie_id))
    print(closer_user)

    return recommended_movies_name

def recommend(rate):
    cluster = readCluster()
    userId = random.randint(101, 999)
    new_user[userId] = rate
    print(new_user[userId])
    recommendation = top5Movies(new_user, k, cluster)

    return recommendation