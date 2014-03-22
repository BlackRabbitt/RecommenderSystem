# import unittest
#
#
# class test_calculated_rating(unittest.TestCase):
#     def setUp(self):
#         self.data = {1: [1, 5, -3], 2: [1, 3, 0]}
#         self.result = {3: [49, 217, -105]}
#         self.distance = [35, 14]
#         self.newuser = [0, 3, 0]
#
#     def test_calculate(self):
#         user = 2
#         book = 3
#         recommended_ratings = {}  # format is like: {book1:3, book2:4, .... , bookn: 1}
#         #initially the recommended ratings for each book is zero
#         for m in range(book):
#             recommended_ratings[m] = 0
#         for i in range(user):
#             for j in range(book):
#                 recommended_ratings[j] = recommended_ratings[j] + (self.data[i + 1][j] * self.distance[i])
#         #self.assertEqual(self.result, recommended_ratings)
#
#         # get the position of value 0 in user ratings
#         pos_0_rate = []
#         for i in range(book):
#             if self.newuser[i] == 0:
#                 pos_0_rate.append(i)
#         self.assertEqual(pos_0_rate, [0, 2])
#
#         # get ratings of book that user havn't read yet
#         ratings_to_recommend = {}
#         for each_pos in pos_0_rate:
#             ratings_to_recommend[each_pos] = recommended_ratings[each_pos]
#         self.assertEqual(ratings_to_recommend, {0: 49, 2: -105})
#
#         #sort according to the value such that the book_id at first is most recommended item
#         most_recommendation_first = sorted(ratings_to_recommend, key=ratings_to_recommend.get)
#         self.assertEqual(most_recommendation_first, [2, 0])
#         self.assertEqual(most_recommendation_first[0:1], [2])
#
