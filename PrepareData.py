import random
#prepare data in appropriate format for the recommendation module. Either generate randomly or by any other means.
#return no of user, no of book and prepared data
def prepareData():	
	no_of_user = 5000
	no_of_book = 500
	data = {}
	#generate random ratings for each book for each user
	for i in range(no_of_user):
		rate = []
		for j in range(no_of_book):
			rate.append(random.randint(0,5))
		data[i+1] = rate
	
	return no_of_user, no_of_book, data