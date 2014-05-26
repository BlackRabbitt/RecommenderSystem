RecommenderSystem
=================
#Version 1.2
Recommends list of movies either for user or for test data.

#Features
User can interact with the program via CUI interface, where user can rate each movie. User are allowed to rate from range 0 to 5 and
when user wants program to stop asking for the ratings, he/she can "stop" the program with command <stop>.
Based on this input ratings, program will calculate the recommendation for user.
Recommendation is done on two phase: 1. Clustering, and 2. Collaborative Filtering.

Dependencies
============
#PANDAS INSTALLATION

1. sudo gedit /etc/apt/sources.list
2. deb http://us.archive.ubuntu.com/ubuntu raring main universe
3. sudo apt-get update
4. sudo apt-get install python3-pandas

