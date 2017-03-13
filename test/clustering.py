#!/usr/bin/pythoni
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

stopwords = nltk.corpus.stopwords.words('french')
content = get_content_article()
#print(content.values())
#tokenize_only = tokenize_only(content.values())

#tf-idf representation
tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=200000, min_df=0.2, stop_words=stopwords, use_idf=True, tokenizer=tokenize_only, ngram_range=(1,3))
tfidf_matrix = tfidf_vectorizer.fit_transform(content.values())

print('TF-IDF done')
#print(tfidf_matrix.shape)
terms = tfidf_vectorizer.get_feature_names()

#MeanShift algorithms
dist = 1 - cosine_similarity(tfidf_matrix)
ms = MeanShift()
ms.fit(dist)
clusters = ms.labels_.tolist()
cluster_centers = ms.cluster_centers_

print('We actually have %d clusters' %len(cluster_centers))

connect('azotTest')
gpcl = [{'cluster':vlue , 'article':TestArticle.objects[idx] } for (idx, vlue) in enumerate(clusters)]
#storage of the cluster_id with the article_id in them in a new collection, named Event
#if connect('azotTest'):
#    print('Connected to the database')
#    for cl in gpcl:
#        cluster = TestCluster()
#        cluster.cluster_number = cl['cluster']
#        cluster.article_id = cl['article_id']
#        cluster.save()
#    print('Storage of clusters done')
    
#get the keywords per cluster (and add the keywords in the new collection GroupEvent
for el1 in gpcl:
    print(el1['article'].title) 
	    

