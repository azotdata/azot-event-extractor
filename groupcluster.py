#!/usr/bin/python
from mongoengine import *
from bson.objectid import ObjectId

class GroupCluster(Document):
    _id = IntField()
    keywords = DictField()
    meta = {'collection':'clusters','strict':False}
