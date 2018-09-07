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

**Question:** Write an aggregation query to sum up the population by state and put the result in a field called population.

**Answer:**

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
### Using $avg
**Question:** Write an aggregation expression to calculate the average population of a zip code by state.

**Answer:**
```
use zipCodes
db.zips.aggregate([
    {"$group":
        {
            "_id": "$state", {
            "average_pop": {$avg: "$pop"}
        }
    ])
```
### Using $addToSet

**Question:** Write an aggregation query that will return the postal codes that cover each city. The results should look like this:
```
{
    "_id" : "CENTREVILLE",
    "postal_codes" : [
        "22020",
        "49032",
        "39631",
        "21617",
        "35042"
    ]
},
```

**Answer:**
```
use zipCodes
db.zips.aggregate([
    {"$group":
        {
            "_id": "$city", {
            "postal_codes": {$addToSet: "$_id"}
        }
    ])
```
#### Note:

This query spits out a cursor that looks like:
```
{ "_id" : "TALKEETNA", "postal_codes" : [ "99676" ] }
{ "_id" : "SOUTH NAKNEK", "postal_codes" : [ "99670" ] }
{ "_id" : "SOLDOTNA", "postal_codes" : [ "99669" ] }
{ "_id" : "QUINHAGAK", "postal_codes" : [ "99655" ] }
{ "_id" : "MEKORYUK", "postal_codes" : [ "99630" ] }
```
To make it easier to read and confirm I had the write query, I added the ```.pretty()``` to the end of the query to make it look like the example. Not all cities have more than one postal code. You'll have to iterate through the cursor to find one such as:
```
{
	"_id" : "VANCOUVER",
	"postal_codes" : [
		"98686",
		"98661",
		"98663",
		"98660",
		"98682",
		"98664"
	]
}
```
**Don't add the ```.pretty()``` to your quiz answer or it will be wrong.**

### Using $push
Using ```$push``` is similar to ```$addToSet```, however, ```$push``` pushing items into an array without checking if the value is already there.
**Question:** Given the zip code data set, would you expect the following two queries to produce the same result or different results?
```
db.zips.aggregate([{"$group":{"_id":"$city", "postal_codes":{"$push":"$_id"}}}])
```
```
db.zips.aggregate([{"$group":{"_id":"$city", "postal_codes":{"$addToSet":"$_id"}}}])
```
**Answer:** Same result, because zip codes are unique values. Whether the operation is ```$push``` or ```$addToSet``` it doesn't matter. If zip codes happened to be reused from state-to-state, then using ```$push``` wouldn't be a good idea because it would push the same zip code as many times as it appeared in the data set.

### Using $max and $min
**Question:** Write an aggregation query that will return the population of the postal code in each state with the highest population.

**Answer:**
```
use zipCodes
db.zips.aggregate([
    {"$group":
        {
            "_id": "$state",
            "pop": {$max: "$pop"}
        }
    }

])
```
### Double $group Stages
**Question:** Given the collection:
```
> db.fun.find()
{ "_id" : 0, "a" : 0, "b" : 0, "c" : 21 }
{ "_id" : 1, "a" : 0, "b" : 0, "c" : 54 }
{ "_id" : 2, "a" : 0, "b" : 1, "c" : 52 }
{ "_id" : 3, "a" : 0, "b" : 1, "c" : 17 }
{ "_id" : 4, "a" : 1, "b" : 0, "c" : 22 }
{ "_id" : 5, "a" : 1, "b" : 0, "c" : 5 }
{ "_id" : 6, "a" : 1, "b" : 1, "c" : 87 }
{ "_id" : 7, "a" : 1, "b" : 1, "c" : 97 }
```
and the following aggregation query:
```
db.fun.aggregate([{$group:{_id:{a:"$a", b:"$b"}, c:{$max:"$c"}}}, {$group:{_id:"$_id.a", c:{$min:"$c"}}}])
```
What values are returned?
**Answers:** 52 and 22. 
