import time
import threading

from recommender.CollaborativeFiltering import *
from dataset.testData import test_data
from recommender import no_of_items
from recommender.dataAPI import getItemName


class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.checksum = 1

    def run(self):
        recommend(1)
        self.checksum = 0


def recommend(test=0):
    rate = []
    new_user = {}
    ratings = 5
    k = 3
    n = 10
    start_time = time.time()
    #clustering is done
    cluster = kMean(k)
    cluster_time = time.time() - start_time

    #collaborative filtering is done.
    start_time = time.time()
    if test == 1:
        recommendation = collaborativeFiltering(test_data, k, cluster, n)
    else:
        for j in range(no_of_items):
            rate.append(random.randint(0, ratings))
        new_user[1000] = rate
        recommendation = collaborativeFiltering(new_user, k, cluster, n)
    print("\nClustering, Total Time Elapsed: ", cluster_time, "secs\n")
    print("\nRecommendation, Total Time Elapsed: ", time.time() - start_time, "secs\n")
    print("Recommended Movies are:\n")

    for i in range(n):
        print(i + 1, ":", '[', recommendation[i], ']', getItemName(recommendation[i]))

if __name__ == '__main__':
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
        time.sleep(2)
