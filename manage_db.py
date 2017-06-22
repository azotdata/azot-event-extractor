import couchdb
from mongoengine import *
from utils import *

class ManageConnection():
    def __init__(self):
        self.db_name = DB_NAME

    def connection(self,db_server):
        if db_server=='mongodb':
            connect(self.db_name)
        elif db_server=='couchdb':
            server = couchdb.Server()
            if server[self.db_name]:
                return server[self.db_name]
            else:
                server.create(self.db_name)
                return server[self.db_name]

class DbInterface():
    def __init__(self):
        pass

    def check_article_url(self):
        pass

    def _set_article(self, article):
        pass

    def save_article(self, article):
        pass

    def update_article(self):
        pass

    @staticmethod
    def sw_exist():
        pass

    def set_stopwords(self,sw_path):
        pass

    @staticmethod
    def get_all_stopwords():
        pass

    def set_dataclusters(self,cluster_id,keywords,title):
        pass

    @staticmethod
    def remove_cluster_content():
        pass

