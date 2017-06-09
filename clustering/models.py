"""
This script contains definition of document stored in mongo DB
"""
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *
from datetime import datetime
from bson.objectid import ObjectId

class Stopword(Document):
    """
        Class for storing stopwords objects
    """
    meta = {
        'collection': 'stopword'
    }

    lang = StringField(max_length=50)
    word = StringField(max_length=50)


class TopicWord(Document):
    """
        Class for storing important words, called topic, per cluster
    """
    meta = {
        'collection': 'topic_word'
    }

    word = StringField()
    topic = StringField()
    count = IntField()
    stopword = BooleanField()
    to_delete = BooleanField()


class Article(Document):
    """
        Represents articles stored in DB. Used for both reading and inserting articles datas
    """
    meta = {
        'collection': 'articles'
    }

    #keywords = StringField()
    _id = ObjectId()
    num_cluster = IntField()
    pub_date = StringField()
    source = StringField()
    text = StringField()
    title = StringField()
    #tokens = StringField()
    #cluster = None

    def set_article(self,article):
        self.source=article.url
        self.title=article.title
        self.text=article.text
        if article.publish_date:
            self.pub_date = str(article.publish_date[0].date())
        else:
            self.pub_date = str(article.publish_date)

class ClusteringReport(Document):
    """
        Stores details after clustering.
    """
    meta = {
        'collection': 'clustering_report'
    }

    date = StringField()
    count = IntField()
    iterations = IntField()
    nb_cluster = IntField()
    cluster_list = DictField()



class ClusteringResume(Document):
    """
        Stores main elements useful for each cluster
    """
    meta = {
        'collection': 'clustering_resume',
        'strict': False
    }

    _id = IntField()
    #resumes = DictField()
    keywords = DictField()
    cluster_title = StringField()


class ClusteringTagged(Document):
    """
        Stores important words of a same topic which are generated after manual classification.
    """
    meta = {
        'collection': 'clustering_tagged'
    }

    nb_cluster_before = IntField()
    nb_cluster_after = IntField()
    tags = StringField()
    clusters = DictField()

