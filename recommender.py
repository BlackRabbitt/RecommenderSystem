from KMean import *
from CollaborativeFiltering import *

#generate random new user
rate = []
new_user = {}
no_of_item = 1682
ratings = 5
for j in range(no_of_item):
	rate.append(random.randint(0,ratings))

new_user[1000] = rate

k = 4
n = 5
#clustering is done
cluster = kMean(k)
#collaborative filtering is done.
recommendation = collaborativeFiltering(new_user, k, cluster, n)

print (recommendation)