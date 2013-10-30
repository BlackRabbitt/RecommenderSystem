from KMean import *
from CollaborativeFiltering import *

#generate random new user
rate = []
new_user = {}
for j in range(500):
	rate.append(random.randint(0,5))

new_user[9292] = rate

k = 5
n = 5
#clustering is done
cluster = kMean(k)
#collaborative filtering is done.
recommendation = collaborativeFiltering(new_user, k, cluster, n)

print (recommendation)