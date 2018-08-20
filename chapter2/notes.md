# Sort, Skip, and Limit

MongoDB always processes these three in a certain order:

1. Sort
* Skip
* Limit

Let's look at the code.

```python
query = {}
try:
    cursor = scores.find(query).skip(4)
    cursor.limit(1)
    cursor.sort([('student_id', pymongo.ASCENDING),
                 ('score', pymongo.DESCENDING)])

except Exception as e:
    print "Unexpected error:", type(e), e
```
I wrote the ```skip``` first, then ```limit``` and finally ```sort```. However, MongoDB returned ```sort```, then ```skip```, then ```limit```. It doesn't matter what order the code calls. The DB will wait until ```sort``` then execute the rest. Thus, if the code were true to the order of operations from the DB, then it would look like this:

```python
query = {}
try:
    cursor.sort([('student_id', pymongo.ASCENDING),
                 ('score', pymongo.DESCENDING)])
    cursor.limit(1)
    cursor = scores.find(query).skip(4)
except Exception as e:
    print "Unexpected error:", type(e), e
```
I guess writing the code out like this will avoid confusion moving forward.
