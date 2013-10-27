
class Clustering:
	#datatype for cluster representing single cluster
	#create a datastructure for cluster
	#e.g.,
	#----------------------------------------------
	# cluster_no. |   user_id   |     centroid 
	#      0      |  [1, 5, n]  |   [3,5,0,.....,1]
	#----------------------------------------------
	# p.s. only user starts from 1
	def __init__(self, cluster_no, user_id):
		self.cluster_no = cluster_no
		self.user_list = [user_id]
		self.centroid = data[user_id]