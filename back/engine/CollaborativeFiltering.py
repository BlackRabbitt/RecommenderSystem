from back.engine.KMean import *
from back.engine import no_of_items

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
    # format of calculated_weights : {book1: rating1, book2: rating2, .... , bookn: ratingn}
    calculated_weights = {}
    # initially the recommended ratings for each book is zero
    for i in range(no_of_items):
        calculated_weights[i] = 0
    # calculate the ratings for user
    for j in range(no_of_items):
        for i in range(len(cluster_user_list)):
            calculated_weights[j] = calculated_weights[j] + (
                data[cluster_user_list[i]][j] * euclideanDistance(user_ratings, data[cluster_user_list[i]]))
    # get the position of value 0 in user_ratings.
    pos_0_ratings = []
    for i in range(no_of_items):
        if user_ratings[i] == 0:
            pos_0_ratings.append(i)

    # get ratings of book that user have not read yet
    ratings_to_recommend = {}
    for each_pos in pos_0_ratings:
        ratings_to_recommend[each_pos] = calculated_weights[each_pos]

    # print("calculated weights:", ratings_to_recommend)
    # twentyNumber for tau-a statistic test
    # twentyNumbers = [24, 395, 212, 55, 1, 113, 664, 6, 682, 890, 32, 435, 570, 820, 549, 341, 655, 796, 554, 16]
    # for i in range(20):
    #     print("calculate weights for twentyNumbers [",twentyNumbers[i],"]: ", ratings_to_recommend[twentyNumbers[i]])

    # sort according to the value such that the book_id at last is most recommended item
    most_recommendation_last = sorted(ratings_to_recommend, key=ratings_to_recommend.get)
    return most_recommendation_last[0:n]