#!/usr/bin/python
################################################################################
#Author: Antsa Raharimanantsoa
#Description: Classification using clustering algorithm
#Creation_date: March 2017
################################################################################

import nltk
from mongoengine import *
from document import *
from lib import *
from algo_clustering import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import cluster
from operator import itemgetter
from itertools import groupby
import logging
from datetime import datetime
import time

log_name = datetime.now().strftime("%Y%m%d_%H%M")
logging.basicConfig(filename='log/clusters/' + log_name + '.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %I:%M:%S %p')

stopwords = nltk.corpus.stopwords.words('french')
stopwords += nltk.corpus.stopwords.words('english')

"""Retrieve all contents for the clustering"""
content = get_content_article()
logging.info("Retrieve all articles for the classification")

"""tf-idf representation"""
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000,
                                 min_df=0.2,stop_words=stopwords,
                                    use_idf=True,ngram_range=(1,3)
                                    ,tokenizer=tokenize_only)
tfidf_matrix = tfidf_vectorizer.fit_transform(content.values())

print('---- TF-IDF done ----')
logging.info("TF-IDF done, clustering ongoing ...")

"""Here is the call of the method of classification, defined in algo_clustering.py """
dist = 1 - cosine_similarity(tfidf_matrix)
clusters = meanshift(dist)
#numbers=[110,115,120,125,130,135]

"""Test of Kmeans (number of clusters must be detected in advance)"""
#kmeans(tfidf_matrix,numbers)

"""Test of Hierarchicla algorithm"""
#hierarchical(dist,content.keys())

"""Add the cluster ID to the collection articles, and update the collection cLusters"""
if connect(DATABASE_NAME):
    print('Connected to the database')
    gp_tokens = []
    gp_clusters = [{'cluster':vlue,
                    'article_id':content.keys()[idx]} for (idx,vlue) in enumerate(clusters)]
    for each_art in NewArticle.objects:
        for idents in gp_clusters:
            if each_art.id == idents['article_id']:
                each_art.update(set__num_cluster=idents['cluster'])
                gp_tokens.append((each_art.tokens,idents['cluster']))
    print('Articles successfully matched to their clusters')
    logging.info('Articles successfully matched to their clusters')

    GroupCluster.objects().delete()
    sorted_tokens = sorted(gp_tokens, key=itemgetter(1))
    gather_tokens = groupby(sorted_tokens, key=itemgetter(1))
    gp_keywords = [{'cluster':k,
                    'keywords':keywords(''.join([elms1 for (elms1,elms2) in v]), 15)} for k, v in gather_tokens]
    for kwds in gp_keywords:
        g_cluster = GroupCluster()
        g_cluster._id = kwds['cluster']
        g_cluster.keywords = kwds['keywords']
        g_cluster.article_lists=[art_id['article_id'] for art_id in gp_clusters if art_id['cluster'] == kwds['cluster']]
        g_cluster.save()
    print('Stored to the collection clusters')
    logging.info('Stored to the collection clusters')
