import random
#prepare data in appropriate format for the recommendation module. Either generate randomly or by any other means.
def prepareData(no_of_user, no_of_book):
	data = {}
	rate = []*no_of_book
	#generate random ratings for each book for each user
	for i in range(no_of_book):
		rate.append(random.randint(0,5))
	for i in range(no_of_user):
		data[i] = rate

	return no_of_user, no_of_book, data