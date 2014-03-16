import random, math
import dataAPI
from KMean import *

# Traditional Collaborative Filtering.
# parameter-1: new_user = new user for whom cf is done.
# parameter-2: k = no. of cluster
# parameter-3: n = no. of recommendation to be returned
# return: n no. of recommended book_id
def collaborativeFiltering(new_user, k, cluster, n):
	# get the key and ratings of new user
	user_key = list(new_user)[0]
	user_ratings = new_user[user_key]
	
	# find the closest cluster to the user
	cluster_no = calculateSimilarities(user_ratings, cluster, k)
	# find the recommended ratings for the user w.r.t each and every user in the cluster
	cluster_user_list = cluster[cluster_no].user_list
	# format of predicted_ratings : {book1: rating1, book2: rating2, .... , bookn: ratingn}
	predicted_ratings = {}
	# initially the recommende ratings for each book is zero
	for i in range(no_of_item):
		predicted_ratings[i] = 0
	# calculate the ratings for user
	for j in range(no_of_item):
		for i in range(len(cluster_user_list)):
			predicted_ratings[j] = predicted_ratings[j] + (data[cluster_user_list[i]][j] * euclideanDistance(user_ratings, data[cluster_user_list[i]]) )
	# get the position of value 0 in user_ratings.
	pos_0_ratings = []
	for i in range(no_of_item):
		if user_ratings[i] == 0:
			pos_0_ratings.append(i)

	# get ratings of book that user havn't read yet
	ratings_to_recommend = {}
	for each_pos in pos_0_ratings:
		ratings_to_recommend[each_pos] = predicted_ratings[each_pos]
	#sort according to the value such that the book_id at first is most recommended item
	print("predicted Ratings:", ratings_to_recommend)
	# most_recommendation_first = sorted(ratings_to_recommend, key=ratings_to_recommend.get)
	# return most_recommendation_first[0:n]
	return ratings_to_recommend[0:n]
