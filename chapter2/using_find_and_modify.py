import pymongo

# gets the next number in a sequence
def get_next_sequence_number(name):
    connection = pymongo.MongoClient("mongodb://localhost")

    db = connection.test
    counters = db.counters

    try:
        counter = counters.find_one_and_update(filter={'type':name},
                                               update={'$inc':{'value':1}},
                                               upsert=True,
                                               return_document=pymongo.ReturnDocument.AFTER)
    except Exception as e:
        print "Exception: ", type(e), e

    counter_value = counter['value']
    return counter_value


print get_next_sequence_number('uid')
print get_next_sequence_number('uid')
print get_next_sequence_number('uid')
