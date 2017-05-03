# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nltk
from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

from models import *

class CustomClusterizer():

    def __init__(self, articles):
        self.articles = articles
        self.classifier = cluster.KMeans()
        self.calculate_intial_clusters()
        self.vectorizer = TfidfVectorizer(
            max_features = 200000,
            tokenizer = self.custom_tokenizer
        )

    def custom_tokenizer(self, text):
        stopwords = []
        for stopword in Stopword.objects.all():
            stopwords.append(stopword.word)

        tokens = [word for word in nltk.word_tokenize(text) if word.isalpha() and len(word) > 2]

        filtered_tokens = []
        for token in tokens:
            if token not in stopwords:
                filtered_tokens.append(token)

        return filtered_tokens

    def calculate_intial_clusters(self):
        articles_count = len(self.articles)
        self.update_nb_cluster(int(articles_count / 100)+1)


    def update_nb_cluster(self, nb_clusters):
        self.nb_clusters = nb_clusters
        self.classifier.n_clusters = self.nb_clusters


    def compute_kmeans(self, matrix):
        print("\t\tNb Clusters: "+str(self.nb_clusters))
        return self.classifier.fit_predict(matrix)


    def vectorize(self, texts):
        return self.vectorizer.fit_transform(texts)


    def clusterize(self, articles=None, nb_clusters=None):

        if articles is not None:
            self.articles = articles
            self.calculate_intial_clusters()

        if nb_clusters is not None:
            self.update_nb_cluster(nb_clusters)

        articles_text = []
        for article in self.articles:
            articles_text.append(article.text)


        # Converting to Frequency Matrix
        print("\t\tVectorizing texts")
        text_matrix = self.vectorize(articles_text)

        # Performing clustering
        print("\t\tClustering")
        cluster_labels = self.compute_kmeans(text_matrix)

        # Mapping Articles to Clusters
        print("\t\tMapping to articles")
        iter = 0
        clusters = {}
        for label in cluster_labels:
            if label not in clusters:
                clusters[label] = []

            clusters[label].append(self.articles[iter])
            iter += 1

        return clusters

    def multi_clusterize(self, articles=None, nb_clusters=None, iterations=1,  human_readable_return=True):

        if articles is not None:
            self.articles = articles
            self.calculate_intial_clusters()

        if nb_clusters is not None:
            self.update_nb_cluster(nb_clusters)

        original_articles = self.articles

        articles_batchs = []
        articles_batchs.append(self.articles)

        print("Starting clustering with " + str(iterations) + " iterations and " + str(self.nb_clusters) + " clusters")

        for iteration in range(0, iterations):
            print("\r\nRunning iteration number " + str(iteration + 1))

            batch_iteration = 0
            clusters = {}
            for articles_batch in articles_batchs:
                if (len(articles_batch) > self.nb_clusters):
                    print("\tBatch number  " + str(batch_iteration + 1) + "/" + str(len(articles_batchs)))

                    clusters[batch_iteration] = self.clusterize(articles_batch, self.nb_clusters)
                    batch_iteration += 1

            clusters = self.consolidate_clusters(clusters)

            # preparing articles for next iteration
            #articles_batchs = []
            #for key, value in clusters.iteritems():
            #    articles_batchs.append(value)
#
            #if human_readable_return:
            #    clusters = self.humanize_clusters(clusters)

            ClusteringReport(date=str(datetime.now()), count=len(clusters), iterations=10, nb_cluster=self.nb_clusters, cluster_list=clusters).save()



        #self.articles = original_articles


        return clusters


    def consolidate_clusters(self, clusters):
        consolidated_clusters = {}
        iterator = 0

        for cluster_key, cluster in clusters.iteritems():
            for key, article_batch in cluster.iteritems():
                consolidated_clusters[str(iterator)] = article_batch
                iterator += 1

        return consolidated_clusters


    def humanize_clusters(self, clusters):
        readable_clusters = {}
        iterator = 0

        for cluster_key, cluster in clusters.iteritems():
            if cluster_key not in readable_clusters:
                readable_clusters[cluster_key] = []

            for article in cluster:
                readable_clusters[cluster_key].append(article.title)
                iterator += 1

        return readable_clusters

    def __str__(self):
        return "<CustomClusterizer>"