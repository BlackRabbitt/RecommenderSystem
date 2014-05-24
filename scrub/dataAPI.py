import pandas as pd
from engine import no_of_items, no_of_users, itemData

# read each Item from u.item and convert it in appropriate format
def readForItem():
    item = {}
    item_cols = ['item_id', 'item_name']
    temp_item = pd.read_csv(itemData, sep='|', names=item_cols, usecols=range(2), encoding="ISO-8859-1")
    # convert the format of item as {item_id:item_name}
    for i in range(len(temp_item)):
        item[temp_item.item_id[i] - 1] = temp_item.item_name[i]
    return item


# prepare data in appropriate format for the recommendation module. Either generate randomly or by any other means.
# return no of user, no of book and prepared data
def prepareData(inputFile, test=0):
    data = {}
    if test == 1:
        data.update({1: [0] * no_of_items})
    else:
        for i in range(no_of_users):
            data.update({i + 1: [0] * no_of_items})
    ratings_cols = ['user_id', 'item_id', 'rating']
    ratings = pd.read_csv(inputFile, sep='\t', names=ratings_cols, usecols=range(3))
    for row in ratings.values:
        data[row[0]][row[1] - 1] = row[2]
    return data


# input: item_id
# returns: item_name
def getItemName(item_id):
    item = readForItem()
    item_name = item[item_id - 1]
    return item_name

