import pandas as pd 
import os
from collections import defaultdict

PATH = 'dataset/'
os.chdir(PATH)
no_of_users = 943
no_of_items = 1682
total_ratings = 100000

# read each Item from u.item and convert it in appropriate format
def readForItem():
	item = {}
	item_cols = ['item_id', 'item_name']
	temp_item = pd.read_csv('u.item', sep='|', names = item_cols, usecols = range(2),encoding = "ISO-8859-1" )
	# convert the format of item as {item_id:item_name}
	for i in range(len(temp_item)):
		item[temp_item.item_id[i]-1] = temp_item.item_name[i]
	return item

# prepare data in appropriate format for the recommendation module. Either generate randomly or by any other means.
# return no of user, no of book and prepared data
def prepareData( inputFile, test=0 ):
	ratings = {}
	data = {}
	if test==1:
		data.update({1: [0]*no_of_items})
	else:
		for i in range(no_of_users):
			data.update({i+1: [0]*no_of_items})
	ratings_cols = ['user_id', 'item_id', 'rating']
	ratings = pd.read_csv( inputFile, sep='\t', names = ratings_cols, usecols = range(3) )
	for row in ratings.values:
		data[row[0]][row[1]-1] = row[2]
	# pdf = ratings.pivot("user_id", "item_id").fillna(0)
	# print ("pdf", pdf)
	# data = {k: v.tolist() for k,v in pdf.iterrows()}
	return data, no_of_users, no_of_items

# input: item_id 
# returns: item_name
def getItemName(item_id):
	item = readForItem()
	item_name = item[item_id-1]
	return item_name

