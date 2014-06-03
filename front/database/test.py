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
        # sys.exit(1)

if __name__ == '__main__':
    main()