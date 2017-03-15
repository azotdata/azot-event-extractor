#!/usr/bin/python

from mongoengine import *

class TestArticle(Document):
#     article_id = StringField()
    title = StringField(required=True)
    text = StringField(required=True)
    pub_date = DateTimeField()
    location = StringField()
    source = StringField(required=True)
    tokens = StringField()
    meta = {'collection': 'testarticles','strict':False}
