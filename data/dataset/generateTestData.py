import pandas as pd

from data.scrub.dataAPI import no_of_items


if __name__ == '__main__' :
    inputFile = {0:"u1.base", 1:"u2.base", 2:"u3.base", 3:"u4.base", 4:"u5.base"}
    ratings = {}
    data = {}
    u = 13
    data[u] = [0] * no_of_items
    for i in range(5):
        ratings_cols = ['user_id', 'item_id', 'rating']
        ratings = pd.read_csv(inputFile[i], sep='\t', names=ratings_cols, usecols=range(3))
        for row in ratings.values:
            if row[0] == u:
                data[row[0]][row[1] - 1] = row[2]
    twentyNumbers = [24, 395, 212, 55, 1, 113, 664, 6, 682, 890, 32, 435, 570, 820, 549, 341, 655, 796, 554, 16]
    print(data)
    for i in range(20):
        print(twentyNumbers[i],":",data[u][twentyNumbers[i]])
        data[u][twentyNumbers[i]] = 0
    print(data)