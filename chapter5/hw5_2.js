use test
db.zips.aggregate([
  {$match:
    {state:{$in:["NY","CA"]}}
  }
  ,
  {$group:
     {
       _id:{city:"$city",state:"$state"},
       city_pop:{$sum:"$pop"}
     }
  }
  ,
  {$match:
    {city_pop:{$gt:25000}}
  }
  ,
  {$group:
     {
        _id:1,
        average:{$avg:"$city_pop"}
     }
  }

])
