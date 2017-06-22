# -*- coding: utf-8 -*-

""""
Script which contains all class definition related to COUCHDB database
"""

from manage_db import *
from mongoengine import *
from utils import *

class Connection(ManageConnection):
    """
        Manage connection to database
    """
    def __init__(self,db_server):
        self.db_server = db_server
        ManageConnection.__init__(self)

    def connect(self):
        self.connection(self.db_server)

""" -------------------------------------------- """
""" ----Database connection must be done here--- """
if DB_SERVER=='couchdb':
    from db_couchdb import *
elif DB_SERVER=='mongodb':
    from db_mongodb import *

connecting = Connection(DB_SERVER)
connecting.connect()
""" -------------------------------------------- """

class Article(Document):
    """
        Represents articles stored in DB. Used for both reading and inserting articles datas
    """
    meta = {
        'strict': False,
        'collection': 'articles'
    }
    num_cluster = IntField()
    pub_date = StringField()
    source = StringField()
    text = StringField()
    title = StringField()

    @staticmethod
    def check_article_url(url):
        if not Article.objects(source=url):
            return True

    def _set_article(self, article):
        self.source = article.url
        self.title = article.title
        self.text = article.text
        if article.publish_date:
            self.pub_date = str(article.publish_date[0].date())
        else:  # just in case publishing date cannot be retrieved, stores 'None'
            self.pub_date = str(article.publish_date)

    def save_article(self,article):
        self._set_article(article)
        self.save()

    @staticmethod
    def get_all_articles():
        return Article.objects.all()

    def update_article(self,cluster_key):
        self.update(set__num_cluster=cluster_key)

class Stopword(Document):
    """
        Class for storing stopwords objects
    """
    meta = {
        'collection': 'stopword'
    }

    lang = StringField(max_length=50)
    word = StringField(max_length=50)

    @staticmethod
    def sw_exist():
        if Stopword.objects:
            return True

    @staticmethod
    def set_stopwords():
        word_list = stopwords_list(SW_PATH)
        sw_list = []
        for lang, word in word_list.iteritems():
            for each_word in word:
                sw_list.append(Stopword(**{"lang": lang, "word": each_word}))
        Stopword.objects.insert(sw_list)

    @staticmethod
    def get_all_stopwords():
        return Stopword.objects.all()

class ClusteringResume(Document):
    """
        Stores main useful elements for each cluster
    """
    meta = {
        'collection': 'clustering_resume',
        'strict': False
    }

    _id = IntField()
    keywords = DictField()
    cluster_title = StringField()

    def set_dataclusters(self,cluster_id,keywords,title):

        #cluster_list = []
        #for i in range(cluster_number):
        self._id = cluster_id
        self.keywords = keywords
        self.cluster_title = title
        self.save()

    @staticmethod
    def remove_cluster_content():
        return ClusteringResume.objects.delete()

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
