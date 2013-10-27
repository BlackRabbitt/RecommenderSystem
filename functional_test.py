#we are going to implement TDD (Test Driven Development) approach for our recommendation problem.
import unittest
from Recommender import Clustering
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
class test_clustering(unittest.TestCase):
	pass