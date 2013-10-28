#we are going to implement TDD (Test Driven Development) approach for our recommendation problem.
import unittest
from Recommender import *
from PrepareData import prepareData

#Data Preparation Test
class test_prepareData(unittest.TestCase):	
	def test_no_of_user_and_book(self):	
		no_of_user = 10
		no_of_book = 5	
		self.assertIn(no_of_user, prepareData(no_of_user, no_of_book))
		self.assertIn(no_of_book, prepareData(no_of_user, no_of_book))

	def check_the_max_of_rate(self, rate_list):
		found_max = max(rate_list)
		if found_max > 5:
			raise "Assertion Error: Rating shouldnot exceed 5"

	def test_format_of_data(self):
		no_of_user = 10
		no_of_book = 5	
		user, book, data = prepareData(no_of_user, no_of_book)
		self.assertEqual(no_of_book, len(data[2]))
		self.assertEqual(no_of_user, len(data))
		self.check_the_max_of_rate(data[3])
#Clustering Test
class test_kMean(unittest.TestCase):
	def test_single_cluster(self):
		cluster_obj = Cluster(1, 5)
		self.assertIn(5, cluster_obj.user_list)

	def test_multiple_cluster(self):
		cluster_list = []
		for i in range(3):
			cluster_list.append(Cluster(i, i+1))
		self.assertIn(2, cluster_list[1].user_list)

#test for the initial cluster
class test_cluster(unittest.TestCase):
	def test_len_random_generated_user_equals_with_k(self):
		k = 2
		self.assertEqual(k, len(initCluster(k, 10)))

	def test_random_generated_user_is_unique(self):		
		k = 2		
		no_of_user = 10
		init_user, cluster = initCluster(k, no_of_user)
		#check if the user_list is unique or not.
		self.assertEqual(len(init_user), len(set(init_user)))
		#check the centroid of each unique initial user
		centroid_obj = Cluster(1, init_user[1])
		self.assertEqual(cluster[1].centroid, centroid_obj.centroid)

class test_euclideanDistance(unittest.TestCase):
	def test_if_distance_is_equal_with_calculated_distance(self):
		user_centroid = [1, 0, 2, 3, 0]
		cluster_centroid = [3, 2, 5, 1, 3]
		#manually calculated and type cast in int.
		dist = 5
		distance_between_two_user = euclideanDistance(user_centroid, cluster_centroid)
		self.assertEqual(dist, int(distance_between_two_user))

	def test_to_find_the_closest_cluster(self):
		user_centroid = [1, 0, 2, 3, 0]
		random_user, cluster = initCluster(2, 3)
		centroid1 = Cluster(0, random_user[0])
		centroid2 = Cluster(1, random_user[1])
		dist1 = euclideanDistance(user_centroid, centroid1.centroid)
		dist2 = euclideanDistance(user_centroid, centroid2.centroid)
		if dist1 < dist2:
			min_dist = 0
		else:
			min_dist = 1
		
		close_cluster = calculateSimilarities(user_centroid, cluster, 2)
		self.assertEqual(min_dist, close_cluster)

	def test_to_add_user_to_its_respective_cluster(self):
		user_id = 139
		user_centroid = [1, 0, 2, 3, 0]
		random_user, cluster = initCluster(2, 10)
		close_cluster = calculateSimilarities(user_centroid, cluster, 2)
		self.assertEqual(len(cluster[close_cluster].user_list), 1)
		addUserToCluster(user_id, cluster, close_cluster)
		self.assertEqual(len(cluster[close_cluster].user_list), 2)
		#add again the same user, and the size will not increase.
		addUserToCluster(user_id, cluster, close_cluster)
		self.assertEqual(len(cluster[close_cluster].user_list), 2)
	
	def test_add_each_user_from_data_to_its_respective_cluster(self):
		#populate the cluster with the existing data sets.
		#should return [cluster] of lenght equals k
		k = 3
		cluster = populateCluster(k)
		self.assertEqual(len(cluster), k)

	def test_if_centroid_is_a_mean_for_each_cluster(self):
		cluster = populateCluster(3)
		centroid1 = changeCentroid(cluster)
		#self.assertEqual(len(centroid1), 5)	
		