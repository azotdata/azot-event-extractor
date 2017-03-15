#!/usr/bin/pythoni
import nltk
import newspaper
from newspaper import Article
from mongoengine import *
from pymongo import MongoClient
from article import NewArticle
from groupcluster import GroupCluster
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
#get the keywords per cluster (and add the keywords in the new collection Event)
if connect('azotData'):
    print('Connected to the database')
    gpcl = [(NewArticle.objects[idx].tokens,vlue) for (idx, vlue) in enumerate(clusters)]
    sorted_input = sorted(gpcl, key=itemgetter(1))
    groups = groupby(sorted_input, key=itemgetter(1))
    gpcluster = [{'type':k, 'items':keywords(''.join([elm1 for (elm1,elm2) in v]), 15)} for k, v in groups]
