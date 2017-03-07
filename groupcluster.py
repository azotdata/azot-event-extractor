#!/usr/bin/python
from mongoengine import *
from bson.objectid import ObjectId

class GroupCluster(Document):
    cluster_number = IntField()
    article_id = ObjectId()
    meta = {'collection':'clusters','strict':False}
