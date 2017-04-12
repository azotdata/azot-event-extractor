#!/usr/local/python
################################################################################
#Author: Antsa Raharimanantsoa
#Description: Contain the definition of the document collection in the database
#Creation_date: March 2017
################################################################################
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
    meta = {'collection': ARTICLE_COLLECTION,'strict': False}

    def set_articles(self, title, text, source):
        self.title = title
        self.text = text
        self.source = source

class ErrorDownload(Document):
    _id = ObjectId()
    urls = StringField()
    meta = {'collection' : BAD_URL_COLLECTION, 'strict': False}

class GroupCluster(Document):
    _id = IntField()
    keywords = DictField()
    title = StringField()
    article_lists = ListField()
    meta = {'collection':CLUSTER_COLLECTION,'strict':False}

class Event(Document):
    _id = ObjectId()
    event_name = StringField()
    sources_list = ListField()
    titles_list = ListField()
