import pymongo
import sys

# establish a connection to the database
connection = pymongo.MongoClient("mongodb://localhost")

# get a handle to the reddit database
db=connection.reddit
# use the stories collection
stories = db.stories

def find():
    print "find, reporting for duty"

    # query db for titles that contain apple or google in them with case insensitive option
    query = {'title':{'$regex':'apple|google', '$options':'i'}}
    # project only title, no _id or other data
    projection = {'title': 1, '_id': 0}

    # query db, add findings to cursor var, and catch any execptions
    try:
        cursor = stories.find(query, projection)
    except Exception as e:
        print "Unexpected error:", type(e), e

    # loop over the cursor var and print out each entry
    for doc in cursor:
        print doc

# call the find function
find()
