# Task: Write a program in the language of your choice that will remove the grade of type "homework"
# with the lowest score for each student from the dataset in the handout. Since each document is one grade,
# it should remove one document per student.

import pymongo
# gets the next number in a sequence
def delete_lowest_hw_grade():
    # set up connection to mongo running on localhost
    connection = pymongo.MongoClient("mongodb://localhost")

    # using the students database
    db = connection.students

    # using the grades collection
    grades = db.grades

# Steps to complete homework task

# 1. Select all homework grades, stort students then homework stores from lowest to highest, and store in a variable
    query = {'type': 'homework'}
    projection = {'_id': 0, 'student_id': 1, 'score': 1}
    try:
        cursor = grades.find(query, projection)
        #cursor.limit(10)
        cursor.sort([('student_id', pymongo.ASCENDING),
                     ('score', pymongo.DESCENDING)])

    except Exception as e:
        print "Exception: ", type(e), e

# 2. Loop through the variable and delete the first grade for each student in the document

    list = []
    count = 0
    for item in cursor:
        list.append(item)
    for i in list:
        if count % 3 == 0:
            print list[count]
        count += 1

    print " "
    print list[390:401]

delete_lowest_hw_grade()
