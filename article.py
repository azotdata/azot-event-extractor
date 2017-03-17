#!/usr/bin/python
from mongoengine import *
from bson.objectid import ObjectId

class NewArticle(Document):
    _id = ObjectId()
    title = StringField(required=True)
    text = StringField(required=True)
    pub_date = StringField()
    location = StringField()
    source = StringField(required=True)
    tokens = StringField()
    num_cluster = IntField()
    meta = {'collection': 'articles','strict':False}
