#!/usr/local/python
from mongoengine import *
from bson.objectid import ObjectId
from lib import *

class NewArticle(Document):
    _id = ObjectId()
    title = StringField(required=True)
    text = StringField(required=True)
    pub_date = StringField()
    location = StringField()
    source = StringField(required=True)
    tokens = StringField()
    num_cluster = IntField()
    meta = {'collection': ARTICLE_COLLECTION,'strict':False}

class GroupCluster(Document):
    _id = IntField()
    keywords = DictField()
    title = StringField()
    article_lists = ListField()
    meta = {'collection':CLUSTER_COLLECTION,'strict':False}
