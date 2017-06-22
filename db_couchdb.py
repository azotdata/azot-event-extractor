# -*- coding: utf-8 -*-

""""
Script which contains all class definition related to COUCHDB database
"""

from manage_db import *

class Connection(ManageConnection):
    """
    Manage connection to database
    """
    def __init__(self,db_server):
        self.db_server = db_server
        ManageConnection.__init__(self)

    def connect(self):
        return self.connection(self.db_server)

""" -------------------------------------------- """
""" ----Database connection must be done here--- """
if DB_SERVER=='couchdb':
    from db_couchdb import *
elif DB_SERVER=='mongodb':
    from db_mongodb import *

connecting = Connection(DB_SERVER)
COUCHDB = connecting.connect()
""" -------------------------------------------- """

from couchdb.mapping import Document, TextField, IntegerField, DictField, ViewField

class Article(Document):
    """
        Represents articles stored in DB. Used for both reading and inserting articles datas
    """

    type = TextField()
    title = TextField()
    text = TextField()
    source = TextField()
    pub_date = TextField()
    cluster = IntegerField()
    by_source = ViewField('source', '''\
        function(doc) {
            if (doc.type=='article'){emit(doc.source, doc);};
        }''')
    by_article = ViewField('article', '''\
        function(doc) {
            if (doc.type=='article'){emit(doc);};
        }''')

    @staticmethod
    def check_article_url(url):
        #permanent view
        result = COUCHDB.view('source/by_source')
        if not list(result[url]):
            return True

    def _set_article(self, article):
        self.type = 'article'
        self.source = article.url
        self.title = article.title
        self.text = article.text
        if article.publish_date:
            self.pub_date = str(article.publish_date[0].date())
        else:  # just in case publishing date cannot be retrieved, stores 'None'
            self.pub_date = str(article.publish_date)

    def save_article(self, article):
        self._set_article(article)
        self.store(COUCHDB)

    @staticmethod
    def get_all_articles():
        options = {"include_docs":True}
        result = Article.view(COUCHDB,'article/by_article',**options)
        return list(result)

    def update_article(self, cluster_key):

        self.cluster = cluster_key
        self.store(COUCHDB)

class Stopword(Document):
    """
        Class for storing stopwords objects
    """
    type = TextField()
    lang = TextField()
    word = TextField()
    by_stopword = ViewField('stopword', '''\
            function(doc) {
                if (doc.type=='stopword'){emit(doc.lang, doc);};
            }''')

    def sw_exist(self):
        result = COUCHDB.query(self.by_stopword.map_fun)
        if list(result):
            return True

    def set_stopwords(self):
        word_list = stopwords_list(SW_PATH)
        sw_list = []
        for lang, word in word_list.iteritems():
            for each_word in word:
                sw_list.append(Stopword(type='stopword',lang=lang,word=each_word))
        #return sw_list
        COUCHDB.update(sw_list)

    def get_all_stopwords(self):
        options = {"include_docs": True}
        result = Stopword.view(COUCHDB, 'stopword/by_stopword', **options)
        return result


class ClusteringResume(Document):
    """
        Stores main useful elements for each cluster
    """
    type = TextField()
    _id = TextField()
    keywords = DictField()
    cluster_title = TextField()

    def set_dataclusters(self,cluster_id,keywords,title):
        self.type = 'cluster'
        self._id = cluster_id
        self.keywords = keywords
        self.cluster_title = title
        self.store(COUCHDB)

    def remove_cluster_content(self):
        result = COUCHDB.query(self.by_cluster.map_fun)
        for element in list(result):
            elem = COUCHDB.get(element.id)
            COUCHDB.delete(elem)
