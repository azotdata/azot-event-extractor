from pymongo import MongoClient
from bson.son import SON

db = MongoClient().azotData

db.articles.aggregate([
{$group:{"_id":"$title","title":{$first:"$title"},"count":{$sum:1}}},
{$match:{"count":{$gt:1}}},
{$project:{"title":1,"_id":0}},
{$group:{"_id":null,"duplicateNames":{$push:"$title"}}},
{$project:{"_id":0,"duplicateNames":1}}
])

db.articles.find({}, {myCustomKey:1}).sort({_id:1}).forEach(function(doc){
    db.myCollection.remove({_id:{$gt:doc._id}, myCustomKey:doc.myCustomKey});
})
