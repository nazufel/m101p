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
    projection = {'_id': 1, 'student_id': 1, 'score': 1}
    try:
        cursor = grades.find(query, projection)
        #cursor.limit(10)
        cursor.sort([('student_id', pymongo.ASCENDING),
                     ('score', pymongo.DESCENDING)])

    except Exception as e:
        print "Exception: ", type(e), e

# 2. Loop through the variable and delete the first grade for each student in the document

    all_list = []
    low_list = []
    count = 0
    for item in cursor:
        all_list.append(item)
    for i in all_list:
        if count % 2 != 0:
            low_list.append(all_list[count]['_id'])
        count += 1

    for i in low_list:
        db.grades.delete_one({'_id': i})

    #print(low_list[:])

delete_lowest_hw_grade()
