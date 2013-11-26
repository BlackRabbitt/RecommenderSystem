from KMean import *
from CollaborativeFiltering import *
from dataAPI import getItemName
import time
import threading
#generate random new user
rate = []
new_user = {}
no_of_item = 1682
ratings = 5
for j in range(no_of_item):
	rate.append(random.randint(0,ratings))
new_user[1000] = rate

class myThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.checksum = 1

	def run(self):
		recommend(4)
		self.checksum = 0

def recommend(k):
	global new_user
	n = 5
	start_time = time.time()
	#clustering is done
	cluster = kMean(k)
	print ("k=",k,"\nClustering, Total Time Elapsed: ", time.time()-start_time, "secs\n")
	#collaborative filtering is done.
	start_time = time.time()
	recommendation = collaborativeFiltering(new_user, k, cluster, n)
	print ("k=",k,"\nRecommendation, Total Time Elapsed: ", time.time()-start_time, "secs\n")
	print("k=",k,"Recommended Movies are:\n")
	for i in range(n):
		print (i+1,":",getItemName(recommendation[i]))
	
if __name__ == '__main__':
	#thread1 = myThread()
	#thread1.start()
	recommend(1)
	recommend(4)

