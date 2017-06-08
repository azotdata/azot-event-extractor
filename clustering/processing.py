# -*- coding: utf-8 -*-
"""
This script contains classes definition for managing clusters: creation, identification, evaluation ...
"""

from __future__ import unicode_literals

import nltk
from nltk.tag import StanfordPOSTagger
from nltk.tag import StanfordNERTagger
from sklearn import cluster
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import metrics
import operator
from operator import itemgetter
from itertools import groupby


from models import *


class ArticleManager():
    """
        Parent class used of both Clusterizer and Merger.
        Defines method for them
    """

    @staticmethod
    def get_articles_text(articles):
        """
            Gets a list of all articles.
            For best result, title is added three time
        """

        articles_text = []
        for article in articles:
            content = article.title + " " + article.title + " " + article.title + " " + article.text
            content = content.replace("\r", "").replace("\n", "")
            articles_text.append(content)

        return articles_text

    @staticmethod
    def get_articles_by_cluster(articles):
        """
            Gets articles per cluster.
        """

        table = []
        for article in articles:
            table.append((article, article.num_cluster))

        sorted_table = sorted(table, key=itemgetter(1))
        table = groupby(sorted_table, key=itemgetter(1))
        article_table = [{'cluster': k,
                          'articles': [elms1 for (elms1, elms2) in v]} for k, v in table]

        return article_table


class CustomClusterizer(ArticleManager):
    """
        This clas aims to execute the clustering.
    """

    def __init__(self, articles):
        self.articles = articles
        self.classifier = cluster.KMeans()
        self.calculate_intial_clusters()
        self.vectorizer = TfidfVectorizer(
            max_features = 200000,
            tokenizer = self.custom_tokenizer
        )

    # Customizes tokenization.
    @staticmethod
    def custom_tokenizer(text):

        stopwords = []
        for stopword in Stopword.objects.all():
            stopwords.append(stopword.word)

        tokens = [word for word in nltk.word_tokenize(text) if word.isalpha() and len(word) > 2]

        filtered_tokens = []
        for token in tokens:
            if token not in stopwords:
                filtered_tokens.append(token)

        return filtered_tokens

    # Calculate probable number of clusters
    def calculate_intial_clusters(self,articles=None):
        if articles is None:
            articles_count = len(self.articles)
        else:
            articles_count = len(articles)
        self.update_nb_cluster(int((articles_count * 5) / 100) + 1)

    # updates cluster number
    def update_nb_cluster(self, nb_clusters):
        self.nb_clusters = nb_clusters
        self.classifier.n_clusters = self.nb_clusters

    # calls the K-means method
    def compute_kmeans(self, matrix):

        print("\t\tNb Clusters: "+str(self.nb_clusters))
        return self.classifier.fit_predict(matrix)

    # vectorizes texts
    def vectorize(self, texts):

        return self.vectorizer.fit_transform(texts)

    # execute clustering once
    def clusterize(self, articles=None, nb_clusters=None):

        # can be used on standalone
        if articles is not None:
            self.articles = articles
            self.calculate_intial_clusters()

        if nb_clusters is not None:
            self.update_nb_cluster(nb_clusters)

        # get all texts
        articles_text = self.get_articles_text(self.articles)

        # vectorization with tf-idf
        print("\t\tVectorizing texts")
        text_matrix = self.vectorize(articles_text)

        # K-means
        print("\t\tClustering")
        cluster_labels = self.compute_kmeans(text_matrix)

        # Retrieves articles text for each cluster
        print("\t\tMapping to articles")
        iter = 0
        clusters = {}
        for label in cluster_labels:
            if label not in clusters:
                clusters[label] = []

            clusters[label].append(self.articles[iter])
            iter += 1

        return clusters

    # Iterates clustering, first with all articles, next in each cluster, and so on, until iteration number is reached
    def multi_clusterize(self, articles=None, iterations=1, human_readable_return=False):#nb_clusters=None,

        if articles is not None:
            self.articles = articles
            self.calculate_intial_clusters()

        original_articles = self.articles

        # Each cluster is a batch. First, we have unique batch
        articles_batchs = []
        articles_batchs.append(self.articles)

        print("Starting clustering with " + str(iterations) + " iterations and " + str(self.nb_clusters) + " clusters")

        # looping according to iteration number
        for iteration in range(0, iterations):
            print("\r\nRunning iteration number " + str(iteration + 1))

            batch_iteration = 0
            clusters = {}
            for articles_batch in articles_batchs:
                self.calculate_intial_clusters(articles_batch)
                #if len(articles_batch) > self.nb_clusters:
                print("\tBatch number  " + str(batch_iteration + 1) + "/" + str(len(articles_batchs)))
                clusters[batch_iteration] = self.clusterize(articles_batch, self.nb_clusters)
                batch_iteration += 1
            clusters = self.consolidate_clusters(clusters)

            # in order to proceed to next iteration, drain previous batch
            articles_batchs = []
            for key, value in clusters.iteritems():
                articles_batchs.append(value)

        # For debug, this simplifies the reading of results
        if human_readable_return:
            clusters = self.humanize_clusters(clusters)

        # Set the cluster number in which each article belongs
        self.update_articles(clusters)

        # Necessary only in case two iterations are execute in the same script
        self.articles = original_articles

        return clusters

    # Re-organizes datas in cluster as dictionnary for further usage
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
                readable_clusters[str(cluster_key)] = []

            for article in cluster:
                readable_clusters[str(cluster_key)].append(article.title)
                iterator += 1

        return readable_clusters

    def update_articles(self, clusters):
        for cluster_key, cluster in clusters.iteritems():
            for article in cluster:
                article.update(set__num_cluster=cluster_key)
        return None

    def __str__(self):
        return "<CustomClusterizer>"


class EvaluateClusterizer(ArticleManager):
    """
    This class aims to evaluate the clustering method - needs to be improved
    """
    def __init__(self):
        self.classifier = cluster.MeanShift()
        self.vectorizer = TfidfVectorizer(max_features=200000,
                                          tokenizer=CustomClusterizer.custom_tokenizer)

    def vectorize(self,texts):
        return self.vectorizer.fit_transform(texts)

    def similarity_mesure(self,articles=None):
        articles = self.get_articles_by_cluster(articles)
        measure_clusters = {}
        for article in articles:
            articles_texts = []
            for each_article in article['articles']:
                articles_texts.append(each_article.text)
            print("\t\tVectorizing texts")
            text_matrix = self.vectorize(articles_texts)

            measure_clusters[article['cluster']] = cosine_similarity(text_matrix)
        return measure_clusters

    # It's a test if mean_shift is applied in each clusters
    def mean_shift_clusterize(self, articles):
        length_clusters = {}
        for article in articles:
            articles_texts = []
            for each_article in article['articles']:
                articles_texts.append(each_article.text)
            print("\t\tVectorizing texts")
            text_matrix = self.vectorize(articles_texts)
            normalized_matrix = self.similarity_mesure(text_matrix)
            mean_shift_classifier = cluster.MeanShift()
            try:
                mean_shift_classifier.fit(normalized_matrix)
            except ValueError:
                print('Too close bandwidth')
                length_clusters[article['cluster']] = 0
                continue

            cluster_labels = mean_shift_classifier.labels_
            cluster_centers = mean_shift_classifier.cluster_centers_

            length_clusters[article['cluster']] = len(cluster_centers)

        return length_clusters


class CustomMerger(ArticleManager):
    """
        Gets keywords per cluster and aims to gather those which are similar
    """

    def __init__(self):
        self.vectorizer = CountVectorizer(
            max_features = 200000,
            tokenizer = CustomClusterizer.custom_tokenizer
        )


    def invert_dict(self, original_dict):
        return {v: k for k, v in original_dict.iteritems()}

    # determines most valued words
    def extract_values(self, tokens, count):
        real_count = len(tokens.values())
        if count > real_count:
            count = real_count

        return dict(sorted(tokens.iteritems(), key=operator.itemgetter(1), reverse=True)[:count])

        return articles_text

    # occurrence of a token in a matrix
    def normalize_tokens(self, labels, matrix):

        lines = matrix.shape[0]
        cols  = matrix.shape[1]
        labels = self.invert_dict(labels)

        token_list = {}
        for line in range(0, lines):
            for col in range(0, cols):
                if matrix[line, col] != 0:
                    label = labels[col]

                    if label not in token_list:
                        token_list[label] = matrix[line, col]
                    else:
                        token_list[label] += matrix[line, col]

        return token_list


    def token_frequency(self, tokens, precision=4):

        token_sum   = float(sum(tokens.values()))

        token_frequencies = {}
        for key, value in tokens.iteritems():
            frequency = round(value/token_sum, precision)
            token_frequencies[key] = frequency

        return token_frequencies

    # tokens frequency in corpus
    def tokenize(self, text):

        result = self.vectorizer.fit_transform(text)
        return self.normalize_tokens(self.vectorizer.vocabulary_, result)

    # mean of token frequency
    def tokenize_frequency(self, text):

        result = self.vectorizer.fit_transform(text)
        tokens = self.normalize_tokens(self.vectorizer.vocabulary_, result)
        return self.token_frequency(tokens)

    # Classifies texts using the frequency or occurrence of tokens
    def tokenize_clusters(self, clusters, comparison_sample=10, use_frequency=True):

        working_clusters = {}
        for cluster_label, cluster_list in clusters.iteritems():
            cluster_label = str(cluster_label)

            print("Working on cluster " + cluster_label)
            if cluster_label not in working_clusters:
                working_clusters[cluster_label] = {}

            texts  = self.get_articles_text(cluster_list)
            if use_frequency:
                tokens = self.tokenize_frequency(texts)
            else:
                tokens = self.tokenize(texts)
            working_clusters[cluster_label] = self.extract_values(tokens, comparison_sample)
        self.save_clusters(working_clusters)
        return working_clusters

    # Stores clusters with their keywords in DB
    def save_clusters(self, working_clusters):
        ClusteringResume.objects().delete()
        st = StanfordPOSTagger('french.tagger')
        for cluster_label, token_values in working_clusters.iteritems():
            new_token_values = {}
            cluster_tag = st.tag(token_values)
            for (word,tag) in cluster_tag:
                if tag in ('NPP','NC', 'N'):
                    word_value = [b for a,b in token_values.iteritems() if a == word]
                    new_token_values[word]=word_value[0]
                else:
                    pass
            cluster_title = max(new_token_values)
            ClusteringResume(_id=cluster_label, keywords=working_clusters[cluster_label], cluster_title=cluster_title).save()
        return cluster_title

    # Manually names a selection of keywords
    def process_manual(self, tokenized_clusters, classified_clusters = {}, known_tags = []):

        unclassified_clusters = {}

        for key, value in tokenized_clusters.iteritems():
            print("Cluster: " + str(value))
            print("Known tags: " + str(known_tags))
            print("Saisir un tag (ou 'ignore' pour ignorer le cluster. Il ne sera pas traité.) :")
            tag = raw_input("--> ")
            tag = tag.lower()

            if tag == '' or tag == 'ignore':
                unclassified_clusters[key] = value

            else:
                if tag not in classified_clusters:
                    classified_clusters[tag] = {}
                    known_tags.append(tag)

                for item in value.iteritems():
                    word = item[0]
                    if word not in classified_clusters[tag]:
                        classified_clusters[tag][word] = 0

                    classified_clusters[tag][word] += 1

            print(" ")

        return classified_clusters, unclassified_clusters, known_tags

    def __str__(self):
        return "<CustomMerger>"



class TopicHandler():
    """
        Manages topics (general theme) and keywords.
        Each topic is associated in keywords'weight
    """

    # Saves topics in DB
    def save_words(self, labelised_wordbags):

        for topic, words in labelised_wordbags.iteritems():
            for word, count in words.iteritems():

                result = TopicWord.objects(word=word, topic=topic).first()

                if result is not None:
                    result.count += count
                    result.save()
                else:
                    TopicWord(word=word, topic=topic, count=count, stopword=False, to_delete=False).save()

    # determines topic according to the list of words given
    def find_topic(self, query_result):

        topic_list = {}
        for index in range(0, len(query_result)):
            topic = query_result[index].topic
            count = query_result[index].count
            if topic not in topic_list:
                topic_list[topic] = count
            else:
                topic_list[topic] += count

        final_topic = None
        if len(topic_list) != 0:
            final_topic = max(topic_list, key=topic_list.get)

        return final_topic, topic_list

    # dtects topic of ensemble of words
    def identify_wordbag(self, wordbag):

        result = TopicWord.objects(word__in=wordbag).all()
        return self.find_topic(result)
