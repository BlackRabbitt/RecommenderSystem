from KMean import *
from CollaborativeFiltering import *
from dataAPI import getItemName
import time
import threading
#generate random new user
class myThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.checksum = 1

	def run(self):
		recommend()
		self.checksum = 0

def recommend():
	rate = []
	new_user = {}
	no_of_item = 1682
	ratings = 5
	for j in range(no_of_item):
		rate.append(random.randint(0,ratings))
	new_user[1000] = rate

	k = 4
	n = 5
	start_time = time.time()
	#clustering is done
	cluster = kMean(k)
	print ("\nClustering, Total Time Elapsed: ", time.time()-start_time, "secs\n")
	#collaborative filtering is done.
	start_time = time.time()
	recommendation = collaborativeFiltering(new_user, k, cluster, n)
	print ("\nRecommendation, Total Time Elapsed: ", time.time()-start_time, "secs\n")
	print("Recommended Books are:\n")
	for i in range(n):
		print (i+1,":",getItemName(recommendation[i]))
	
if __name__ == '__main__':
	thread1 = myThread()
	thread1.start()
	#print ("Loading")
	x = 1
	while(thread1.checksum):
		b = "." * x
		#print (b, end="\r")		
		print ("Loading",b, end='\r')
		x = x + 1
		time.sleep(2)

