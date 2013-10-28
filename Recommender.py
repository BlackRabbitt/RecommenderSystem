import random, math
import PrepareData
no_of_user = 10
no_of_book = 5
user, book, data = PrepareData.prepareData(no_of_user, no_of_book)
class Cluster:
	# datatype for cluster representing single cluster
	# create a datastructure for cluster
	# e.g.,
	# ----------------------------------------------
	#  cluster_no. |   user_id   |     centroid 
	#       0      |  [1, 5, n]  |   [3,5,0,.....,1]
	# ----------------------------------------------
	# p.s. only user starts from 1
	def __init__(self, cluster_no=0, user_id=1):
		self.cluster_no = cluster_no
		self.user_list = [user_id]
		self.centroid = data[user_id]

# Initialize the k cluster for no_of_user
# return: initialized cluster with single user in each
def initCluster(k, no_of_user):	
	random_user = random.sample(range(1, no_of_user),k)
	init_cluster = []*k
	for i in range(k):
		init_cluster.append(Cluster(i, random_user[i]))
	return random_user, init_cluster

# Euclidean Distance: smaller the distance closer they are
# E(x,y)=sqroot[ summation{ sqr( xi - yi ) };i=0:n ]
# Parameter-1: other_user_rating = ratings of other_user
# Parameter-2: centroid = ratings (of center of cluster)
# returns: E(x,y); Distance between user_id and the center of cluster.
def euclideanDistance(user_centroid, cluster_centroid):
	summation = 0
	xi = user_centroid #critics of user as a list
	yi = cluster_centroid
	for i in range(len(xi)):
		summation = summation + (xi[i]-yi[i])**2
	E = math.sqrt(summation)
	return E

# calculate the most similar cluster for a user
# parameter-1: user_centroid = ratings of user.
# parameter-2: cluster = all the clusters.
# parameter-3: k = no. of clusters.
# return: cluster_no. closer to the user
def calculateSimilarities(user_centroid, cluster, k):
	dist = {}
	for i in range(k):
		dist[i] = euclideanDistance(user_centroid, cluster[i].centroid)
	#val, closer_cluster = min((val, idx) for (idx, val) in enumerate(dist))
	closer_cluster = min(dist, key=dist.get)
	return closer_cluster

# add user to its closest cluster.
# parameter-1: user_id = id of the user to be added in the closest cluster
# parameter-2: cluster = cluster
# parameter-3: close_cluster = cluster_no close to the user
# return: new list of user in cluster.
def addUserToCluster(user_id, cluster, close_cluster):
	if user_id not in cluster[close_cluster].user_list:
		cluster[close_cluster].user_list.append(user_id)
	return cluster[close_cluster].user_list