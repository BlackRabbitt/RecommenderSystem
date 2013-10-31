from dataAPI import *
import pandas as pd 
import unittest
import time
#class TestData(unittest.TestCase):
# datset for item
# <item_id, item_name>
'''def test_for_item(self):
	item = readForItem()
	self.assertEqual('Toy Story (1995)', item[0])
	self.assertEqual('Copycat (1995)', item[4])
'''
# dataset for user-rate-item
# data = {user_id:[item#1_rating, item#2_rating, ...., item#3_rating]}
def for_ratings():
	data, a ,b = prepareData()
	print (data)
#self.assertEqual(196, ratings.user_id[0])
#self.assertEqual(100000, len(ratings))
#self.assertEqual(943, len(data))
#self.assertEqual(943, user)

'''
def test_for_get_item(self):
item_name = getItemName(0)
self.assertEqual('Toy Story (1995)', item_name)
'''
for_ratings()