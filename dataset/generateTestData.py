import random
import pickle
from testData import test

if __name__=='__main__':
	rate = []
	new_user = {}
	no_of_item = 1682
	ratings = 5

	for j in range(no_of_item):
		rate.append(random.randint(1,ratings))
	new_user[1323] = rate
