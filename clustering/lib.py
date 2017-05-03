# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import *

import nltk
from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer


def custom_tokenizer(text):
    stopwords = []
    for stopword in Stopword.objects.all():
        stopwords.append(stopword.word)

    tokens = [word for word in nltk.word_tokenize(text) if word.isalpha() and len(word) > 2 ]

    filtered_tokens = []
    for token in tokens:
        if token not in stopwords:
            filtered_tokens.append(token)

    return filtered_tokens


def kmean_clustring(matrix, nb_clusters):
    classifier = cluster.KMeans(n_clusters=nb_clusters)
    return classifier.fit_predict(matrix)


def clusterize(articles, nb_clusters):

    articles_text = []
    for article in articles:
        articles_text.append(article.text)

    # Genrerating tokens with custom tokenizer
    text_vectorizer = TfidfVectorizer(
        max_features=200000,
        tokenizer=custom_tokenizer
    )

    # Converting to Frequency Matrix
    text_matrix = text_vectorizer.fit_transform(articles_text)

    # Performing clustering
    cluster_labels = kmean_clustring(text_matrix, nb_clusters)

    # Mapping Articles to Clusters
    iter = 0
    clusters = {}
    for label in cluster_labels:
        if label not in clusters:
            clusters[label] = []

        clusters[label].append(articles[iter])
        iter += 1

    return clusters


def consolidate_clusters(clusters):
    consolidated_clusters = {}
    iterator = 0

    for cluster_key, cluster in clusters.iteritems():
        for key, article_batch in cluster.iteritems():
            consolidated_clusters[str(iterator)] = article_batch
            iterator += 1

    return consolidated_clusters



def humanize_clusters(clusters):
    readable_clusters = {}
    iterator = 0

    for cluster_key, cluster in clusters.iteritems():
        if cluster_key not in readable_clusters:
            readable_clusters[cluster_key] = []

        for article in cluster:
            readable_clusters[cluster_key].append(article.title)
            iterator += 1

    return readable_clusters


def multi_clusterize(articles, iterations=1, nb_clusters=5, human_readable_return=True):
    articles_batchs = []
    articles_batchs.append(articles)

    print("Starting clustering with " + str(iterations) + " iterations and " +str(nb_clusters)+ " clusters")

    for iteration in range(0, iterations):
        print("Running iteration number "+str(iteration+1))

        batch_iteration = 0
        clusters = {}
        for articles_batch in articles_batchs:
            if( len(articles_batch) > nb_clusters ):
                print("Batch number  " + str(batch_iteration + 1) + "/" + str(len(articles_batchs)))

                clusters[batch_iteration] = clusterize(articles_batch, nb_clusters)
                batch_iteration += 1

        clusters = consolidate_clusters(clusters)

        # preparing articles for next iteration
        articles_batchs = []
        for key, value in clusters.iteritems():
            articles_batchs.append(value)

    if human_readable_return:
            clusters = humanize_clusters(clusters)

    return clusters