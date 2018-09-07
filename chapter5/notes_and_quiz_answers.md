# Notes and Quiz Answers for Chapter 5 - Aggregation Framework

 ```
db.products.aggregate([
    {"$group":
        {
            "_id": "$manufacturer",
            "num_products":{$sum1}
        }
    }
])
```

## Quiz Questions and Notes by Section

### Sample Aggregation Example
**Question:** Write the aggregation query that will find the number of products by category of a collection that has the form:
```
{
    "_id" : ObjectId("50b1aa983b3d0043b51b2c52"),
    "name" : "Nexus 7",
    "category" : "Tablets",
    "manufacturer" : "Google",
    "price" : 199
}
```
**Answer:**
```
db.products.aggregate([
    {"$group":
        {
            "_id": "$category",
            "num_products":{$sum:1}
        }
    }
])
```
**Output:**
```
{ "_id" : "Laptops", "num_products" : 2 }
{ "_id" : "Cell Phones", "num_products" : 1 }
{ "_id" : "Tablets", "num_products" : 7 }
```
### The Aggregation Pipeline*
**Question:** Which of the following are stages in the aggregation pipeline?

**Answer:**
1. Match
* Group
* Skip
* Limit
* Sort
* Project
* Unwind

## Simple Example Expanded
**Question:** How many documents will be in the result set from the aggregate ```db.stuff.aggregate([{$group:{_id:'$c'}}])``` in the collection below?
```
> db.stuff.find()
{ "_id" : ObjectId("50b26f9d80a78af03b5163c8"), "a" : 1, "b" : 1, "c" : 1 }
{ "_id" : ObjectId("50b26fb480a78af03b5163c9"), "a" : 2, "b" : 2, "c" : 1 }
{ "_id" : ObjectId("50b26fbf80a78af03b5163ca"), "a" : 3, "b" : 3, "c" : 1 }
{ "_id" : ObjectId("50b26fcd80a78af03b5163cb"), "a" : 3, "b" : 3, "c" : 2 }
{ "_id" : ObjectId("50b26fd380a78af03b5163cc"), "a" : 3, "b" : 5, "c" : 3 }
```
**Answer:**
The answer is 3, because the ```$group``` stage is only looking for unique values of ```'$c'```, not total instances. This messed me until I realized that ```c``` key in all the documents had three values ranging from 1-3.

### Compound Grouping

**Question:** Given the following collection:
```
db.stuff.find()
{ "_id" : ObjectId("50b26f9d80a78af03b5163c8"), "a" : 1, "b" : 1, "c" : 1 }
{ "_id" : ObjectId("50b26fb480a78af03b5163c9"), "a" : 2, "b" : 2, "c" : 1 }
{ "_id" : ObjectId("50b26fbf80a78af03b5163ca"), "a" : 3, "b" : 3, "c" : 1 }
{ "_id" : ObjectId("50b26fcd80a78af03b5163cb"), "a" : 3, "b" : 3, "c" : 2 }
{ "_id" : ObjectId("50b26fd380a78af03b5163cc"), "a" : 3, "b" : 5, "c" : 3 }
{ "_id" : ObjectId("50b27f7080a78af03b5163cd"), "a" : 3, "b" : 3, "c" : 2 }
```
And the following aggregation query:
```
db.stuff.aggregate([{$group:
             {_id:
              {'moe':'$a',
               'larry':'$b',
               'curly':'$c'
              }
             }
            }])
```
How many documents will be in the result set?

**Answer:** The answer is five, because two of the documents have the same values for ```a,b,c```; otherwise, the unique documents will be returned in as their own document.

### Aggregation Expressions
**Question:** Which of the following aggregation expressions must be used in conjunction with a sort to make any sense?

**Answer:** ```$first``` and ```$last``` need to be ran in conjunction with sort.

### Using $sum

```
use zipCodes
db.zips.aggregate([
    {"$group":
        {
            "_id": {
                "state": "$state"
            },
            "population":{$sum: "$pop"}
        }
    ])
```
**Question:** Write an aggregation query to sum up the population by state and put the result in a field called population.
