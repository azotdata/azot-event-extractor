#!/usr/bin/python
from mongoengine import *
from bson.objectid import ObjectId

class TestCluster(Document):
    cluster_number = IntField()
    article_id = ObjectId()
    meta = {'collection':'testclusters','strict':False}
