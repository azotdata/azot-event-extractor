# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import nltk
from sklearn import cluster
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import operator

from models import *


class ArticleManager():
    """
        Classe parent qui sera utilisée à la fois par le Clusterizer et le Merger.
        Elle définit une méthode commune aux deux.
    """

    @staticmethod
    def get_articles_text(articles):
        """
            Permet d'avoir la liste des contenus des articles.
            Cette méthode ajoute le contenu du titre de l'article plusieurs fois afin d'avoir une pondération.
        """

        articles_text = []
        for article in articles:
            content = article.title + " " + article.title + " " + article.title + " " + article.text
            content = content.replace("\r", "").replace("\n", "")
            articles_text.append(content)

        return articles_text



class CustomClusterizer(ArticleManager):
    """
        Cette classe contient les méthodes permettant de trier les différents textes en fonction des mots qu'on y trouve.
        Les principales méthodes peuvent être utilisées de manière indépendentes.
    """

    def __init__(self, articles):
        self.articles = articles
        self.classifier = cluster.KMeans()
        self.calculate_intial_clusters()
        self.vectorizer = TfidfVectorizer(
            max_features = 200000,
            tokenizer = self.custom_tokenizer
        )

    @staticmethod
    def custom_tokenizer(text):
        """
            Méthode de création des tokens personnalisée.
            Elle est utilisée par la classe 'TfidfVectorizer' à la place de sa méthode par féfaut.
        """

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
        """
            Permet de déterminer le nombre de clusters initiaux à créer en fonction du nombre d'articles fournis.
        """

        articles_count = len(self.articles)
        self.update_nb_cluster(int(articles_count / 100)+1)


    def update_nb_cluster(self, nb_clusters):
        """
            Met à jour le nombre de clusters dans la classe mais aussi dans le vectorizer.
        """
        self.nb_clusters = nb_clusters
        self.classifier.n_clusters = self.nb_clusters


    def compute_kmeans(self, matrix):
        """
            Méthode exécutant la classification KMeans.
        """

        print("\t\tNb Clusters: "+str(self.nb_clusters))
        return self.classifier.fit_predict(matrix)


    def vectorize(self, texts):
        """
            Méthode exécutant la vectorization.
        """

        return self.vectorizer.fit_transform(texts)


    def clusterize(self, articles=None, nb_clusters=None):
        """
            Méthode de base pour clusterizer un groupe de texte.
            Elle ne fait qu'une classification.
        """

        # Traitement des articles s'ils sont passés en paramètre.
        # Permet d'utiliser la méthode en standalone
        if articles is not None:
            self.articles = articles
            self.calculate_intial_clusters()

        if nb_clusters is not None:
            self.update_nb_cluster(nb_clusters)

        # Extraction des textes depuis le corpus
        articles_text = self.get_articles_text(self.articles)

        # Conversion en Matrice de Fréquences
        print("\t\tVectorizing texts")
        text_matrix = self.vectorize(articles_text)

        # Réalisation des clusters
        print("\t\tClustering")
        cluster_labels = self.compute_kmeans(text_matrix)

        # Récupération des articles de chaque cluster
        # On ne garde pas que les textes, car on peut avoir besoin de manipuler les articles par la suite
        print("\t\tMapping to articles")
        iter = 0
        clusters = {}
        for label in cluster_labels:
            if label not in clusters:
                clusters[label] = []

            clusters[label].append(self.articles[iter])
            iter += 1

        return clusters


    def multi_clusterize(self, articles=None, nb_clusters=None, iterations=1,  human_readable_return=False):
        """
            Méthode qui permet une utilisation iterative de la méthode de clusterization.
            A chaque itération, le corpus de textes est divisé en plusieurs clusters.
            A l'itération suivante, chaque cluster est de nouveau divisé en plusieurs clusters.
        """

        # Traitement des articles s'ils sont passés en paramètre.
        # Permet d'utiliser la méthode en standalone
        if articles is not None:
            self.articles = articles
            self.calculate_intial_clusters()

        if nb_clusters is not None:
            self.update_nb_cluster(nb_clusters)

        original_articles = self.articles

        # Chaque cluster est considéré comme un lot d'articles.
        # A l'origine, on n'a qu'un seul lot, le corpus initial d'articles
        articles_batchs = []
        articles_batchs.append(self.articles)

        print("Starting clustering with " + str(iterations) + " iterations and " + str(self.nb_clusters) + " clusters")

        # On boucle pour faire le nombre d'itérations demandées
        final_clusters = []
        for iteration in range(0, iterations):
            print("\r\nRunning iteration number " + str(iteration + 1))

            # Pour chaque itération, on traite l'ensemble des lots d'articles.
            batch_iteration = 0
            clusters = {}
            for articles_batch in articles_batchs:
                if (len(articles_batch) > self.nb_clusters):
                    print("\tBatch number  " + str(batch_iteration + 1) + "/" + str(len(articles_batchs)))

                    clusters[batch_iteration] = self.clusterize(articles_batch, self.nb_clusters)
                    batch_iteration += 1
                else:
                    final_clusters.append(articles_batch)

            # Mise à jour du nombre de clusters à créer
            self.nb_clusters += 1

            clusters = self.consolidate_clusters(clusters)

            # Préparation des articles pour l'itération suivante
            # Ici, on vide la liste des lots d'articles et on crée un nouveau lot pour chaque cluster généré à l'étape précédente.
            articles_batchs = []
            for key, value in clusters.iteritems():
                articles_batchs.append(value)

        # On ajoute les lots d'articles trop petits pour être de nouveau divisés
        cluster_size = len(clusters)
        for item in final_clusters:
            clusters[cluster_size] = item

        # Si nécessaire, on rends la liste plus lisible pour l'utilisateur (Debug surtout)
        if human_readable_return:
            clusters = self.humanize_clusters(clusters)

        # La liste originale d'articles, récupérée avant le traitement, est réassignée ici.
        # Cela permet de faire de nouveaux traitement sur le même jeu d'articles si nécessaire
        # (Un nombre d'itérations différentes par exemple)
        self.articles = original_articles

        return clusters


    def consolidate_clusters(self, clusters):
        """
            Réorganise les clusters sous la forme d'un dictionnaire structuré.
            Utilisés pour fournir des données propres pour les traitements à suivre.
        """

        consolidated_clusters = {}
        iterator = 0

        for cluster_key, cluster in clusters.iteritems():
            for key, article_batch in cluster.iteritems():
                consolidated_clusters[str(iterator)] = article_batch
                iterator += 1

        return consolidated_clusters


    def humanize_clusters(self, clusters):
        """
            Remplace l'objet <Article> par le titre de l'article pour une meilleure lisibilité.
            Utilisé surtout pour le debug et le dev.
        """
        readable_clusters = {}
        iterator = 0

        for cluster_key, cluster in clusters.iteritems():
            if cluster_key not in readable_clusters:
                readable_clusters[str(cluster_key)] = []

            for article in cluster:
                readable_clusters[str(cluster_key)].append(article.title)
                iterator += 1

        return readable_clusters


    def __str__(self):
        return "<CustomClusterizer>"




class CustomMerger(ArticleManager):
    """
        Classe permettant de regrouper les différents clusters en fonction de leurs similitudes
    """

    def __init__(self):
        self.vectorizer = CountVectorizer(
            max_features = 200000,
            tokenizer = CustomClusterizer.custom_tokenizer
        )


    def invert_dict(self, original_dict):
        """
            Inverse la clé et la valeur de chaque élément d'un dictionaire.
        """
        return {v: k for k, v in original_dict.iteritems()}


    def extract_values(self, tokens, count):
        """
            Extrait les X valeurs les plus élevées dans une liste de mots clés pondérés.
        """
        real_count = len(tokens.values())
        if count > real_count:
            count = real_count

        return dict(sorted(tokens.iteritems(), key=operator.itemgetter(1), reverse=True)[:count])

        return articles_text


    def normalize_tokens(self, labels, matrix):
        """
            Détermine le nombre d'occurence de chaque tokens dans une matrice.
        """

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
        """
            Calcule la fréquence d'apparition de chaque token par rapport à l'ensemble des tokens de la liste.
        """

        token_sum   = float(sum(tokens.values()))

        token_frequencies = {}
        for key, value in tokens.iteritems():
            frequency = round(value/token_sum, precision)
            token_frequencies[key] = frequency

        return token_frequencies


    def tokenize(self, text):
        """
            Compte le nombre d'occurence de chaque token sur l'ensemble des documents du corpus.
        """

        result = self.vectorizer.fit_transform(text)
        return self.normalize_tokens(self.vectorizer.vocabulary_, result)


    def tokenize_frequency(self, text):
        """
            Fait la moyenne des occurences de chaque token sur l'ensemble des documents du corpus.
        """

        result = self.vectorizer.fit_transform(text)
        tokens = self.normalize_tokens(self.vectorizer.vocabulary_, result)
        return self.token_frequency(tokens)


    def tokenize_clusters(self, clusters, comparison_sample=10, use_frequency=True):
        """
            Méthode qui permet de convertir un corpus de textes en corpus de groupes de mots pondérés, soit par occurence, soit par fréquence.
        """

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

        return working_clusters


    def process_manual(self, tokenized_clusters, classified_clusters = {}, known_tags = []):
        """
            Méthode qui propose à un utilisateur une succession de groupes de mots et lui demande de définir un sujet (topic).
        """

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
        Classe de gestion des topics et des mots clés.
        Un topic est un thème général, associable à plusieurs articles.
        Chaque topic est associé à plusieurs mots clés pondérés.
    """

    def save_words(self, labelised_wordbags):
        """
            Enregistre les mots clés ainsi que les topics associés.
        """

        for topic, words in labelised_wordbags.iteritems():
            for word, count in words.iteritems():

                result = TopicWord.objects(word=word, topic=topic).first()

                if result is not None:
                    result.count += count
                    result.save()
                else:
                    TopicWord(word=word, topic=topic, count=count, stopword=False, to_delete=False).save()


    def find_topic(self, query_result):
        """
            Calcul le topic le plus probable à partir des mots les plus fréquents.
        """

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


    def identify_wordbag(self, wordbag):
        """
            Permet de trouver le topic d'un ensemble de mots donnés.
        """

        result = TopicWord.objects(word__in=wordbag).all()
        return self.find_topic(result)