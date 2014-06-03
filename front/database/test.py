import sys
from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
    # mongoDb connection
    try:
        c = Connection(host="localhost", port=27017)
        sys.stderr.write("Connection Successfull")
    except ConnectionFailure as e:
        sys.stderr.write("connection unsuccesfull: %s" % e)
        sys.exit(1)

    # Get the database handle to the database named "testDb"
    dbh = c["testDb"]
    assert dbh.connection == c

    # insert document into collection
    user_doc = {
        "username": "sujit",
        "address": "Ktm",
        "gender": "mail"
    }
    dbh.users.insert(user_doc, safe = True)
    print("user_doc document has been added in the users collection")



if __name__ == '__main__':
    main()