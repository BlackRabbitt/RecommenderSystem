# Recommender System
# Author: Sujit Shakya
# @BlackRabbitt$
import random, math
import dataAPI

# no_of_user = no of total user returned from PrepareData funtion
# no_of_item = no of total book returned from PrepareData funtion
# data = prepared data.
data, no_of_user, no_of_item = dataAPI.prepareData()

# K-mean algorithm :
# flag for keeping track of centroid change
centroid_change_flag = 1 # 1 for centroid changing, 0 for centroid not changing
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
	#Choose k random users
	random_user = random.sample(range(1, no_of_user),k)
	init_cluster = []*k
	#initialize k cluster
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
# return: cluster_no. closer to the user and the cluster as a whole.
def calculateSimilarities(user_centroid, cluster, k):
	dist = {}
	# calculate and save the distance between user and each cluster in dist(dictionary)
	for i in range(k):
		dist[i] = euclideanDistance(user_centroid, cluster[i].centroid)
	# val, closer_cluster = min((val, idx) for (idx, val) in enumerate(dist)) # if list is used instead of dictionary
	# find closure cluster to the user.
	closer_cluster = min(dist, key=dist.get)
	return closer_cluster
# add user to its closest cluster.
# parameter-1: user_id = id of the user to be added in the closest cluster
# parameter-2: cluster = cluster
# parameter-3: close_cluster = cluster_no close to the user
# return: new list of user in cluster.
def addUserToCluster(user_id, cluster, close_cluster):
	#check if user is not already present in cluster.
	if user_id not in cluster[close_cluster].user_list:
		#append the user_id in the userlist of the cluster
		cluster[close_cluster].user_list.append(user_id)
	return cluster[close_cluster].user_list

# change the centroid of each cluster so that it is the mean of each cluster
# return the mean centroid for each cluster
def changeCentroid(cluster, k):
	global centroid_change_flag
	before_change = {}
	for i in range(k):
		before_change[i] = cluster[i].centroid
	# loop thru each cluster
	for i in range(k):
		new_centroid = [0]*no_of_item
		# loop thru each user inside that cluster.
		user_size_in_each_cluster = len(cluster[i].user_list)
		for j in range(no_of_item):			
			for l in range(user_size_in_each_cluster):
				new_centroid[j] = new_centroid[j] + data[cluster[i].user_list[l]][j]
			# if bychance there is no user in cluster during intermediate process
			# the centroid is updated to [0,0,0,0,0,0.........]
			try:				
				new_centroid[j] = new_centroid[j]/user_size_in_each_cluster
			except:
				new_centroid[j] = 0
		cluster[i].centroid = new_centroid	

	after_change = {}
	for i in range(k):
		after_change[i] = cluster[i].centroid	

	#check if centroid has been changed or not
	cnt = 0
	for i in range(k):
		if before_change[i] == after_change[i]:
			cnt += 1
	if cnt == k: centroid_change_flag = 0 # unchanged
	else: centroid_change_flag = 1 # changed	

#delete all user from cluster during the intermediate process
def emptyUserListFromCluster(cluster, k):
	for i in range(k):
		cluster[i].user_list = []
		
# k-mean return cluster with respective users.
def kMean(k):
	# step1 : initialize the k cluster
	rand_user, cluster = initCluster(k, no_of_user)
	# step2: calculate the distance between each users and randome generated centroid and place the user
	# to its respective cluster
	while centroid_change_flag:
		for i in range(no_of_user):
			# step3: find cluster closure to the user
			closer_cluster_for_i_user = calculateSimilarities(data[i+1], cluster, k)
			#add user to that cluster
			addUserToCluster((i+1), cluster, closer_cluster_for_i_user)
		# step4: change the centroid of cluster
		changeCentroid(cluster, k)
		if centroid_change_flag == 1:
			emptyUserListFromCluster(cluster, k)		
	return cluster

# End K-mean Clustering
