# -*- coding: utf-8 -*-

""""
This script summerizes how the classes structure must be, whether with mongodb or couchdb.
It's not to be implemented
"""


""" 
from manage_db import *

class Connection(ManageConnection):
    def __init__(self,db_server):
        pass

    def connect(self):
        pass
        
        
        -----------------
#Import of db_couchdb or db_mongodb, according to the config file
#Initialize the connection HERE
        -----------------
        
        
class Article(Document):
    def __init__:
        pass

    def check_article_url(url):
        pass

    def _set_article(self, article):
        pass

    def save_article(self, article):
        pass)

    @staticmethod
    def get_all_articles():
        pass

    def update_article(self, cluster_key):
        pass


class Stopword(Document):
    def sw_exist(self):
        pass

    def set_stopwords(self):
        pass

    def get_all_stopwords(self):
        pass


class ClusteringResume(Document):
    def set_dataclusters(self,cluster_id,keywords,title):
        pass

    def remove_cluster_content(self):
        pass

"""
