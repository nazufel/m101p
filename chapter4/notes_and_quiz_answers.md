# Quiz Answers for Chapter 4

## Dot Notation and Multikey
**Question:** Type the command that you would issue in the Mongo shell to create an index on company, descending.
**Answer:**
```
db.people.createIndex({'work_history.company':-1})
```
## Index Creation Option, Unique
**Question:** Please provide the mongo shell command to create a unique index on student_id, class_id, ascending for the collection students.
**Answer:**
```
db.students.createIndex({'student_id':1, 'class_id':1}, {'unique': true})
```
## Index Creation, Sparse
### Notes
* Sparse creates and index for a specified value, but if a document in the collection doesn't have the specified field, the DB server ignores the missing value and indexes the documents that have the value.

**Question:** What are the advantages of a sparse index? Check all that apply.
**Answer:**
1. The index will be smaller than it would if it were not sparse.
* You can gain greater flexibility with creating Unique indexes.

**Example:**
```
db.students.createIndex({'student_id':1, 'class_id':1}, {'unique': true, 'sparse': true})
```
## Index Creation, Background
* Two types:
    - Foreground
        - Fast
        - Blocks writers and readers in the database
    - Background
        - Slow
        - Doesn't block writers and readers

**Question:** Which things are true about creating an index in the background in MongoDB. Check all that apply.
**Answer:**

* Although the database server will continue to take requests, a background index creation still blocks the mongo shell that you are using to create the index.
* Creating an index in the background takes longer than creating it in the foreground.

## Explain
* Shows what the query optimizer will do before it does it.

**Question:** Which of the following are valid ways to find out which indices a particular query uses? Check all that apply.
**Answer:**

```
db.students.explain().find({'score': {$gt:90}})
```
