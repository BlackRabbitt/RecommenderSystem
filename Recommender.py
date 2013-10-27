import random, math
import PrepareData
user, book, data = PrepareData.prepareData(10, 5)

class Cluster:
	#datatype for cluster representing single cluster
	#create a datastructure for cluster
	#e.g.,
	#----------------------------------------------
	# cluster_no. |   user_id   |     centroid 
	#      0      |  [1, 5, n]  |   [3,5,0,.....,1]
	#----------------------------------------------
	# p.s. only user starts from 1
	def __init__(self, cluster_no=0, user_id=1):
		self.cluster_no = cluster_no
		self.user_list = [user_id]
		self.centroid = data[user_id]

#Initialize the centroids for k cluster.
def initCluster(k, no_of_user):
	random_user = []*k
	random_user = random.sample(range(1, no_of_user),k)
	init_cluster = []*k
	for i in range(k):
		init_cluster.append(Cluster(i, random_user[i]))
	return random_user, init_cluster

#Euclidean Distance: smaller the distance closer they are
#E(x,y)=sqroot[ summation{ sqr( xi - yi ) };i=0:n ]
#Parameter-1: other_user_rating = ratings of other_user
#Parameter-2: centroid = ratings (of center of cluster)
#returns: E(x,y); Distance between user_id and the center of cluster.
def euclideanDistance(user_centroid, cluster_centroid):
	summation = 0
	xi = user_centroid #critics of user as a list
	yi = cluster_centroid
	for i in range(len(xi)):
		summation = summation + (xi[i]-yi[i])**2
	E = math.sqrt(summation)
	return E

def calculateSimilarities(user_centroid, cluster1_centroid, cluster2_centroid):
	pass