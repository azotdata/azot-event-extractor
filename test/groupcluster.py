#!/usr/bin/python
from mongoengine import *

class TestCluster(Document):
    _id = IntField()
    keywords = DictField()
    meta = {'collection':'testclusters','strict':False}
