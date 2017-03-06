#!/usr/bin/python

from mongoengine import *

class NewArticle(Document):
#     article_id = StringField()
     title = StringField(required=True)
     text = StringField(required=True)
     pub_date = StringField()
     location = StringField()
     source = StringField(required=True)
     meta = {'collection': 'articles','strict':False}


     
