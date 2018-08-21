# Task: Write a program in the language of your choice that will remove the grade of type "homework"
# with the lowest score for each student from the dataset in the handout. Since each document is one grade,
# it should remove one document per student.

import pymongo

# function to delete the lowest homework grade for a student
def delete_lowest_hw_grade():
    # set up connection to mongo running on localhost
    connection = pymongo.MongoClient("mongodb://localhost")

    # using the students database
    db = connection.students

    # using the grades collection
    grades = db.grades

### Steps to complete homework task ###

# 1. Select all homework grades, stort students then homework stores from lowest to highest, and store in a variable

    # searching for homework documents
    query = {'type': 'homework'}

    # projecting only the _id, student_id, and the scores
    projection = {'_id': 1, 'student_id': 1, 'score': 1}
    try:
        # runing the quey and projection and assigning to the cursor variable
        cursor = grades.find(query, projection)

        # sorting  student_id in assending order and the scores by decending order
        #+ that way, student_id's are in order and the highest homework score if first for
        #+ each student.
        cursor.sort([('student_id', pymongo.ASCENDING),
                     ('score', pymongo.DESCENDING)])

    except Exception as e:
        print "Exception: ", type(e), e

# 2. Loop through the variable and delete the first grade for each student in the document

    #Note: probably not the best algorithm, but it gets the job done. Python isn't my strongest language.

    # init two lists, one for all stores, and the other for the lowest.
    #+ remember, the lower score is the second for each student.
    all_list = []
    low_list = []

    #init a counter at 0
    count = 0

    # iterate over the cursor and append all values to the all_list
    for item in cursor:
        all_list.append(item)

    # itterate over the list and append every other value to the low_list
    for i in all_list:
        # if the count value is not divisible by two, then it corresponds to an odd number
        #+ that odd number is the index of the lowest score for each student. append that to
        #+ to the new low list.
        if count % 2 != 0:
            low_list.append(all_list[count]['_id'])
        # increase the count by 1
        count += 1

    # iterate over the low_list and remove all the corresponding documents from mongo using the
    #+ the stored _id
    for i in low_list:
        db.grades.delete_one({'_id': i})

# call the function
delete_lowest_hw_grade()
