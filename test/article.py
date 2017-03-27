#!/usr/bin/python
from mongoengine import *
from bson.objectid import ObjectId

class TestArticle(Document):
#     article_id = StringField()
    _id = ObjectId()
    title = StringField(required=True)
    text = StringField(required=True)
    pub_date = StringField()
    location = StringField()
    source = StringField(required=True)
    tokens = StringField()
    num_cluster = IntField()
    meta = {'collection': 'testarticles','strict':False}
