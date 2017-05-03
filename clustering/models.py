# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *


class Stopword(Document):
    meta = {
        'collection': 'stopword'
    }

    lang = StringField(max_length=50)
    word = StringField(max_length=50)


class Article(Document):
    meta = {
        'collection': 'articles'
    }

    keywords = StringField()
    num_cluster = IntField()
    pub_date = StringField()
    source = StringField()
    text = StringField()
    title = StringField()
    tokens = StringField()
    cluster = None

class ClusteringReport(Document):
    meta = {
        'collection': 'clustering_report'
    }

    date = StringField()
    count = IntField()
    iterations = IntField()
    nb_cluster = IntField()
    cluster_list = DictField()