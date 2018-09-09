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

```
db.posts.aggregate([{$unwind:"$comments"},{$group: {_id:"$comment.author", comments:{$sum:1} } },{$sort: {comments: -1} },{$limit: 1}])
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
**Question:** How many documents will be in the result set from the aggregate ```db.stuff.aggregate([{$group:{_id:"$c"}}])``` in the collection below?
```
> db.stuff.find()
{ "_id" : ObjectId("50b26f9d80a78af03b5163c8"), "a" : 1, "b" : 1, "c" : 1 }
{ "_id" : ObjectId("50b26fb480a78af03b5163c9"), "a" : 2, "b" : 2, "c" : 1 }
{ "_id" : ObjectId("50b26fbf80a78af03b5163ca"), "a" : 3, "b" : 3, "c" : 1 }
{ "_id" : ObjectId("50b26fcd80a78af03b5163cb"), "a" : 3, "b" : 3, "c" : 2 }
{ "_id" : ObjectId("50b26fd380a78af03b5163cc"), "a" : 3, "b" : 5, "c" : 3 }
```
**Answer:**
The answer is 3, because the ```$group``` stage is only looking for unique values of ```"$c"```, not total instances. This messed me until I realized that ```c``` key in all the documents had three values ranging from 1-3.

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
              {"moe":"$a",
               "larry":"$b",
               "curly":"$c"
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
To make it easier to read and confirm I had the write query, I added the ```.pretty()``` to the end of the query to make it look like the example. Not all cities have more than one postal code. You"ll have to iterate through the cursor to find one such as:
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
**Don"t add the ```.pretty()``` to your quiz answer or it will be wrong.**

### Using $push
Using ```$push``` is similar to ```$addToSet```, however, ```$push``` pushing items into an array without checking if the value is already there.
**Question:** Given the zip code data set, would you expect the following two queries to produce the same result or different results?
```
db.zips.aggregate([{"$group":{"_id":"$city", "postal_codes":{"$push":"$_id"}}}])
```
```
db.zips.aggregate([{"$group":{"_id":"$city", "postal_codes":{"$addToSet":"$_id"}}}])
```
**Answer:** Same result, because zip codes are unique values. Whether the operation is ```$push``` or ```$addToSet``` it doesn"t matter. If zip codes happened to be reused from state-to-state, then using ```$push``` wouldn"t be a good idea because it would push the same zip code as many times as it appeared in the data set.

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

### Using $project
**Question:** Write an aggregation query with a single projection stage that will transform the documents in the zips collection from this:
```
{
    "city" : "ACMAR",
    "loc" : [
        -86.51557,
        33.584132
    ],
    "pop" : 6055,
    "state" : "AL",
    "_id" : "35004"
}
```
to

```
{
    "city" : "acmar",
    "pop" : 6055,
    "state" : "AL",
    "zip" : "35004"
}
```
**Answer:**
```
use zipcodes
db.zips.aggregate([
    {$project:
        {
            _id:0,
            city: {$toLower:"$city"},
            pop:1,
            state:1,
            zip:"$_id"
        }
    }
])
```
### Using $match

#### Notes
Here"s a multistage aggregation query that was done in the lesson.
```
use zipCodes
db.zips.aggregate([
        {$match:
        {
            "$state": "California"
            }},
        {$group:
            {
                _id: "city",
                population: {$sum: "$pop"},
                zip_codes: {$addToSet: "$_id"}
            }

        },
        {$project:
        {
            _id:0,
            city: "$_id",
            population:1,
            zipcodes:1
            }}
])
```
**Question:**  Write an aggregation query with a single match phase that filters for zipcodes with greater than 100,000 people.

**Answer:**
```
use zipCodes
db.zips.aggregate([
    {$match:
        {pop: {$gt:100000}}
    }
])
```
### Using $text
#### Note:
Running a full text search requires that ```$match``` be the first stage in an aggregation pipeline.
```
db.sentences.aggregate([
    {$match:
        {$text: {$search: "tree rat"}}
    },
    {$sort:
        {score: {$meta: "textScore"}}
    },
    {$project:
        {words:1, _id:0}
    }
])
```
**Question:** Which of the following statements are true about using a $text operator in the aggregation pipeline?

**Answer:**
1. ```$text``` is only allowed in the ```$match``` stage of the aggregation pipeline
* ```$text``` is only allowed within a ```$match``` that is the first stage of the aggregation pipeline.

### Using $sort
#### Notes:
* Disk and memory-based sorts are limited to 100MB
    - Can be used before or after the ```$group``` stage
```
db.zips.aggregate([
    {$match:
        {state: "NY"
    },
    {$group:
        {
            _id: "$city",
            population: {$sum: "$pop"}
        }
    },
    {$project:
        {
            _id:0,
            city, "$_id",
            population:1
        }
    },
    {$sort:
        {
            population:-1
        }
    },
])
```
**Question:** Write an aggregation query with just a sort stage to sort by (state, city), both ascending.

**Answer:**
```
db.zips.aggregate([
    {$sort:
        {
            state:1,
            city: 1
        }
    },
])
```
### Using $skip and $limit
#### Notes:
* ```$skip``` and ```$limit``` require ```$sort``` to be ran first.

```
db.zips.aggregate([
    {$match:
        {state: "NY"
    },
    {$group:
        {
            _id: "$city",
            population: {$sum: "$pop"}
        }
    },
    {$project:
        {
            _id:0,
            city, "$_id",
            population:1
        }
    },
    {$sort:
        {
            population:-1
        }
    },
    {$skip:10},
    {$limit:5}
])
```
**Question:** Suppose a query switched the ```$skip``` and ```$limit``` stages to look like this:
```
db.zips.aggregate([
    {$match:
     {
     state:"NY"
     }
    },
    {$group:
     {
     _id: "$city",
     population: {$sum:"$pop"},
     }
    },
    {$project:
     {
     _id: 0,
     city: "$_id",
     population: 1,
     }
    },
    {$sort:
     {
     population:-1
     }
    },
    {$limit: 5},
    {$skip: 10}
])
```
How many documents do you think will be in the result set?
**Answer:** The answer is zero because limiting to five documents, then skipping ten skips over the rest of the data set.
### Revisiting $first and $last
#### Notes:
* ```$first``` and ```$last``` are ```$group``` stage operators.

```
db.zips.aggregate([
    {$group:
        {
            _id: {state:"$state", city:"$city"},
	        population: {$sum:"$pop"},
        }
    },
    {$sort:
        {
            "_id.state":1,
            "population":-1
        }
    },
    {$group:
        {
	        _id:"$_id.state",
	        city: {$first: "$_id.city"},
	        population: {$first:"$population"}
        }
    }
])
```
**Question:** given the following collection:
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
What would be the value of ```c``` in the result from this aggregation query?
```
db.fun.aggregate([
    {$match:{a:0}},
    {$sort:{c:-1}},
    {$group:{_id:"$a", c:{$first:"$c"}}}
])
```
**Answer:** The answer is ```54```. The first stage matches where documents  ```a``` equals ```0```. There are four and ```c``` equals: 17, 21, 52, and 54. Then sort those in descending order, making 54 first. Lastly, ```$group``` and print the first value of ```c```.

### Using $unwind
#### Notes:
* ```$unwind``` breaks arrays and creates a whole new document for each value in the array.
**Question:** Suppose the following collection:
```
db.people.find()
{ "_id" : "Will", "likes" : [ "physics", "MongoDB", "indexes" ] }
{ "_id" : "Dwight", "likes" : [ "starting companies", "restaurants", "MongoDB" ] }
```
And you unwind the "likes" array of each document. How many documents will you wind up with?
**Answer:** You end up with six documents since the two documents have a total of six items in two arrays.
### $unwind example
```
use blog;
db.posts.aggregate([
    {"$unwind":"$tags"},
    {"$group":
        {
            "_id":"$tags",
            "count":{$sum:1}
        }
    },
    {"$sort":{"count":-1}},
    {"$limit": 10},
    {"$project":
     {_id:0,
      'tag':'$_id',
      'count' : 1
     }
    }
    ])
```
**Question:** Which group operator will enable you to reverse the effects of an unwind?
**Answer:** ```$push``` will add values back into arrays. ```$addToSet``` would also work to create unique arrays, but that assumes the arrays had unique values. In this case, ```$push``` is better because it will add identical values multiple times to an array if applicable.

### Double $unwind
#### Notes:
* ```$unwind``` can be ran as many times as there are arrays for documents ina collection.
**Question:** Can you reverse the effects of a double unwind with the ```$push``` operator?
**Answer:** Yes with two ```$push``` operations.

### Using $out
#### Notes:
* Since MongoDB 2.6 you can run an aggregation framework and use the ```$out``` operator to send the results of the aggregation to a new collection.
```
db.names.aggregate([
    {$group:
        {
            _id:{
                first_name: "$first_name",
                last_name: "$last_name"
                },
            points: {$sum: "$points"}
        }
    },
    {$out: "summary_results"}
])
```
### Aggregation Options
#### Notes:
* explain - query plan
* allowDiskUse - uses up to 100MB to sort
* cursor - sets the cursor size
* Only using the new form of aggregation allows for options: ```aggregate([stage, stage, stage])```

#### Queries:
##### Use Explain:
```
db.zips.aggregate([
    {$group:
        {
            _id: "$state",
            population: {$sum:"$pop"}
        }
    },
    {explain:true}
])
```
##### Use allowDiskUse
```
db.zips.aggregate([
    {$group:
        {
            _id: "$state",
            population: {$sum:"$pop"}
        }
    },
    {allowDiskUse:true}
])
```
**Question:** Which of the following aggregation expressions properly allows disk use when performing aggregation?

**Answer:**
```
db.zips.aggregate([{$group:{_id:"$state", population:{$sum:"$pop"}}}],{allowDiskUse:true})
```
### Python and Aggregation Results

#### Notes:
* Pymongo can return an array of documents with aggregation or can return a cursor
    - Array
    ```python
    import pymongo

    connection = pymongo.MongoClient()
    db = connection.aggregate

    result = db.zips.aggregate([{"$group":{"_id:$state", "population": {"$sum":"$pop"}}}])

    print results
    ```
    - Cursor
    ```python
    import pymongo

    connection = pymongo.MongoClient()
    db = connection.aggregate

    result = db.zips.aggregate([{"$group":{"_id:$state", "population": {"$sum":"$pop"}}}], cursor={})

    print results
    ```
    -  allowDiskUse
    ```python
    import pymongo

    connection = pymongo.MongoClient()
    db = connection.aggregate

    result = db.zips.aggregate([{"$group":{"_id:$state", "population": {"$sum":"$pop"}}}], cursor={}, allowDiskUse=True)

    print results
    ```
**Question** Which of the following statements about aggregation results are true?

**Answer:**
```
In mongoDB 2.6, by default, in the shell, the aggregate method returns a cursor.
```
```
In mongoDB 2.4, by default, PyMongo's aggregate method returns a single document.
```
```
In mongoDB 2.6, by default, PyMongo's aggregate method returns a single document.
```
#### Mapping between SQL and Aggregation
```
+------------------------------------+--------------------------------+
| SQL Terms, Functions, and Concepts | MongoDB Aggregation Operations |
+------------------------------------+--------------------------------+
|WHERE                               | $match                         |       
+------------------------------------+--------------------------------+
|GROUP BY                            | $group                         |
+------------------------------------+--------------------------------+
|HAVING                              | $match                         |  
|------------------------------------+--------------------------------+
|SELECT                              | $project                       |
|------------------------------------+--------------------------------+
|ORDER BY                            | $sort                          |  
|------------------------------------+--------------------------------+
|LIMIT                               | $limit                         |  
|------------------------------------+--------------------------------+
|SUM()                               | $sum                           |           
|------------------------------------+--------------------------------+
|COUNT()                             | $sum                           |
|------------------------------------+--------------------------------+
|join                                | No direct corresponding        |
|                                    | operator, however, the $unwind |
|                                    | operator allows for somewhat   |
|                                    | similar functionality but with |
|                                    | fields embedded within the     |
|                                    | document.*                     |
+------------------------------------+--------------------------------+
```
### Limitatoins in Aggregation Framework
* 100MB limit for pipelines
    - Can get around this with ```allowDiskUse```
* 16MB limit by default in Python
    - Can get around this with using a cursor
* Sharding - There are architectural challenges using aggregation on a sharded DB.
