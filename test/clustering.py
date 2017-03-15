#!/usr/bin/pythoni
###############################################################################################################################################################
#Author: Antsa Raharimanantsoa
#Description: Classification using clustering algorithm
#Dependencies: Requires newspaper, nltk, sickit-learn, pandas to be installed
# git clone https://github.com/codelucas/newspaper for newspaper
#Creation_date: 24/02/2017
##############################################################################################################################################################

import nltk
import newspaper
from newspaper import Article
from mongoengine import *
from pymongo import MongoClient
from article import TestArticle
from groupcluster import TestCluster
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import MeanShift
from lib import *
from operator import itemgetter
from itertools import groupby

stopwords = nltk.corpus.stopwords.words('french')
content = get_content_article()

#tf-idf representation
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.2, stop_words=stopwords, use_idf=True, tokenizer=tokenize_only, ngram_range=(1,3))
tfidf_matrix = tfidf_vectorizer.fit_transform(content.values())

print('TF-IDF done')
terms = tfidf_vectorizer.get_feature_names()

#MeanShift algorithms
dist = 1 - cosine_similarity(tfidf_matrix)
ms = MeanShift()
ms.fit(dist)
clusters = ms.labels_.tolist()
cluster_centers = ms.cluster_centers_

print('We actually have %d clusters' %len(cluster_centers))

connect('azotTest')
#gpcl = [(TestArticle.objects[idx].tokens,vlue) for (idx, vlue) in enumerate(clusters)]
#sorted_input = sorted(gpcl, key=itemgetter(1))
#groups = groupby(sorted_input, key=itemgetter(1))
#gpcluster = [{'type':k, 'items':keywords(''.join([elms1 for (elms1,elms2) in v]), 15)} for k, v in groups]

#print(len(content.keys()))
gp_clusters = [{'cluster':vlue , 'article':content.keys()[idx]} for (idx,vlue) in enumerate(clusters)]
#storage of the cluster_id with the article_id in them in a new collection, named Event
print(gp_clusters)
