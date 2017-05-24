# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from mongoengine import *


class Stopword(Document):
    """
        Classe représentant un Stopword. La langue à laquelle il appartient est identifié.
    """
    meta = {
        'collection': 'stopword'
    }

    lang = StringField(max_length=50)
    word = StringField(max_length=50)


class TopicWord(Document):
    """
        Classe qui stocke les mots les plus présents dans les clusters. 
        Chaque mot est associé à un topic et peut se retrouver plusieurs fois dans la table, associé à d'autre topics.
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
        Classe représentant un article déjà existant dans la base de données.
        Elle est utilisée en Lecture Seule.
        
        READ-ONLY
    """
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
    """
        Classe permettant de stocker les resultat du processus de clusterisation par itérations successives.
        Elle n'est utilisée que pour le debug et le dev.
        
        DEBUG/DEV
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
        Classe permettant de stocker les mots clés les plus employés pour chaque cluster créé à la fin de la phase d'itérations successives.
        Elle n'est utilisée que pour le debug et le dev.

        DEBUG/DEV
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
        Classe permettant de stocker les mots clés issus de la fusion de clusters sous le même topic. 
        Ces données sont générées suite au classement manuel des clusters

        DEBUG/DEV
    """
    meta = {
        'collection': 'clustering_tagged'
    }

    nb_cluster_before = IntField()
    nb_cluster_after = IntField()
    tags = StringField()
    clusters = DictField()

