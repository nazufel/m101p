#!/usr/bin/env python
import pymongo
import time

# It is not necessary to import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the school database
db = connection.school
scores = db.scores


def find():

    print "find(), reporting for duty"

    query = {'type': 'exam'}

    try:
        cursor = scores.findOne(query)

    except Exception as e:
        print "Unexpected error:", type(e), e

    sanity = 0
    for doc in cursor:
        print doc
        sanity += 1
        # sleeping for .1 seconds between printing the next student in data set
        time.sleep(.01)
        if (sanity > 300):
            break


def find_one():

    print "find_one(), reporting for duty"
    query = {'student_id': 10}

    try:
        # quiz one had the answer as doc = scores.find_One(), but this errors out when running the program. 
        doc = scores.find_one(query)

    except Exception as e:
        print "Unexpected error:", type(e), e

    print doc


if __name__ == '__main__':
    print "Printing one"
    find_one()  # Change this to find_one() to run that function, instead.
    print "Printing many"
    #find()
