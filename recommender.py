import time
import threading
import sys

from engine.CollaborativeFiltering import *
from dataset.testData import test_data
from engine import no_of_items, k, n
from scrub.dataAPI import getItemName

user_name = input("Please Enter Your Name : ")
new_user = {}

class myThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.checksum = 1

    def run(self):
        recommend(1)
        self.checksum = 0


def prepare():    
    rate = []
    userId = random.randint(101,999)
    ####################################v1.2#############################
    print("type <0> to skip the movie [havn't watched yet] or type <stop> to stop the ratings.")
    stop = 0
    for j in range(no_of_items):
        if stop == 1:
            break
        print(getItemName(j+1))
        while(1):
            rating = input("rate: ")
            if(rating):
                if rating.lower() == 'stop':
                    stop = 1
                    break
                if 0 <= int(rating) <= 5:
                    rate.append(int(rating))
                    break

                else:
                    print("invalid rating.")
    
    while(len(rate) < no_of_items):
        rate.append(0)
    new_user[userId] = rate 

def readCluster():
    with open('cluster.pkl', 'rb') as input:
        cluster = pickle.load(input)
        return cluster

def recommend(test=0):
    recommendation = {}
    ratings = 5
    start_time = time.time()
    #clustering is done
    # kMean(k)
    cluster = readCluster()
    print("cluster Loaded")
    #collaborative filtering is done.
    start_time = time.time()
    if test == 1:
        recommendation = collaborativeFiltering(test_data, k, cluster, n)
    else:
        recommendation = collaborativeFiltering(new_user, k, cluster, n) #v1.2
    print("\nRecommendation, Total Time Elapsed: ", time.time() - start_time, "secs\n")
    print("Hello", user_name, " We recommend you following movies:\n")

    l=1
    for j in reversed(recommendation):
        print(l, ":", getItemName(j))
        l+=1

def main():
    prepare()
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
    
