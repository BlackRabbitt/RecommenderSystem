import time
import threading
from dataset.testData import test_data

from engine.CollaborativeFiltering import *
from engine import no_of_items, k, n
from scrub.dataAPI import getItemName


# user_name = input("Please Enter Your Name : ")
new_user = {}
data = dataAPI.prepareData(trainingData)


class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.checksum = 1

    def run(self):
        recommend(1)
        self.checksum = 0


def prepare():
    rate = []
    userId = random.randint(101, 999)
    ####################################v1.2#############################
    print("type <0> to skip the movie [havn't watched yet] or type <stop> to stop the ratings.")
    stop = 0
    for j in range(no_of_items):
        if stop == 1:
            break
        print(getItemName(j + 1))
        while 1:
            rating = input("rate: ")
            if rating:
                if rating.lower() == 'stop':
                    stop = 1
                    break
                if 0 <= int(rating) <= 5:
                    rate.append(int(rating))
                    break

                else:
                    print("invalid rating.")

    while len(rate) < no_of_items:
        rate.append(0)
    new_user[userId] = rate


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
        for i in range(len(rating_of_closer_user)):
            if int(rating_of_closer_user[i]) == 5:
                recommended_movies.append(i + 1)
                break
    recommended_movies_name = []
    for each_movie_id in recommended_movies:
        recommended_movies_name.append(getItemName(each_movie_id))

    return recommended_movies_name

def recommend(test=0):
    # recommendation = {}
    # ratings = 5
    # start_time = time.time()
    # clustering is done
    # kMean(k)
    cluster = readCluster()
    if test == 1:
        recommendation = top5Movies(test_data, k, cluster)
    else:
        recommendation = top5Movies(new_user, k, cluster)

    return recommendation

def main():
    # prepare()
    thread1 = myThread()
    thread1.start()
    x = 1
    while thread1.checksum:
        b = "|" * x
        #os.system('clear')
        print(b, end='\r')
        x += 1
        if x == 170:
            x = 1
        time.sleep(60)


if __name__ == '__main__':
    main()