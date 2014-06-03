RecommenderSystem
=================
#Version 1.3
Recommends list of movies for user.

#Features
User can interact with the program via Web interface, where user can rate 20 movie. User are allowed to rate from range 0 to 5 or can leave the field blank
Based on this input ratings, program will calculate the recommendation for user.
Recommendation is done with single stage: Clustering. Collaborative Filtering from v1.2 has been removed temporarily, instead the recommendation is done
by 5 user similar with that user in same cluster.

Dependencies
============
#PANDAS INSTALLATION

1. sudo gedit /etc/apt/sources.list
2. deb http://us.archive.ubuntu.com/ubuntu raring main universe
3. sudo apt-get update
4. sudo apt-get install python3-pandas

#MongoDB

1. sudo apt-get update
2. sudo apt-get install mongodb
3. pip3 install pymongo3
