#!/usr/bin/python
#################################################################
#Author: Antsa Raharimanantsoa
#Description: Classification using clustering algorithm
#Creation_date: 03/2017
#################################################################

import nltk
from mongoengine import *
from article import NewArticle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MeanShift
from lib import *
from operator import itemgetter
from itertools import groupby

class GroupCluster(Document):
    _id = IntField()
    keywords = DictField()
    title = StringField()
    article_lists = ListField()
    meta = {'collection':'clusters','strict':False}

stopwords = nltk.corpus.stopwords.words('english')
content = get_content_article()

#tf-idf representation
tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, use_idf=True, tokenizer=tokenize_only)
tfidf_matrix = tfidf_vectorizer.fit_transform(content.values())

print('TF-IDF done')
#terms = tfidf_vectorizer.get_feature_names()

#MeanShift algorithms
dist = 1 - cosine_similarity(tfidf_matrix)
ms = MeanShift()
ms.fit(dist)
clusters = ms.labels_.tolist()
cluster_centers = ms.cluster_centers_

print('We actually have %d clusters' %len(cluster_centers))
#Add the cluster ID to the collections articles, and populate the new collections CLusters
if connect('azotData'):
    print('Connected to the database')
    gp_tokens = []
    gp_clusters = [{'cluster':vlue , 'article_id':content.keys()[idx]} for (idx,vlue) in enumerate(clusters)]
    for each_art in NewArticle.objects:
        for idents in gp_clusters:
            if each_art.id == idents['article_id']:
                each_art.update(set__num_cluster=idents['cluster'])
                gp_tokens.append((each_art.tokens,idents['cluster']))

    sorted_input = sorted(gp_tokens, key=itemgetter(1))
    gather_tokens = groupby(sorted_input, key=itemgetter(1))
    gp_keywords = [{'cluster':k, 'keywords':keywords(''.join([elms1 for (elms1,elms2) in v]), 15)} for k, v in gather_tokens]
    for kwds in gp_keywords:
        g_cluster = GroupCluster()
        g_cluster._id = kwds['cluster']
        g_cluster.keywords = kwds['keywords']
        g_cluster.save()
