# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import *
from os import listdir
from os.path import isfile, join
from ConfigParser import SafeConfigParser

import nltk


from models import *
from lib import *
from clustering import *

from datetime import datetime


# ----- Start generating Config File ----
# --- Only useful if 'config.ini' isn't present
# --- Code left as a reference
#
# config = SafeConfigParser()
# config.read('config.ini')
# config.add_section('database')
# config.add_section('stopwords')
# config.set('database', 'name', 'azotData')
# config.set('stopwords', 'folder_path', 'data')
#
# with open('config.ini', 'w') as conf_file:
#     config.write(conf_file)
# ----- End generating Config File ----


# Reading Config file
config = SafeConfigParser()
config.read('config.ini')

# Opening database connexion
connect(config.get('database', 'name'))

stopwords_path = config.get('stopwords', 'folder_path')
if Stopword.objects.count() == 0:
    print("No stopwords found. Importing from files.")

    lang_files = [f for f in listdir(stopwords_path) if isfile(join(stopwords_path, f))]

    #Parsing each file to get stopwords
    for lang in lang_files:
        with open(stopwords_path + "/" + lang) as f:
            print("Inserting '"+lang+"' stopwords into collection.")

            word_string = f.read().decode('utf-8')
            word_list = word_string.split("\n")

            for word in word_list:
                word = word.replace("\r", "").lower().encode('utf-8')
                if word != "".encode('utf-8'):
                    Stopword(lang=lang, word=word).save()

            print("Done inserting '" + lang + "' stopwords.")

    print("Done loading stopwords.\r\n")

print("French stopwords found : " + str(Stopword.objects(lang="french").count()) )
print("English stopwords found : " + str(Stopword.objects(lang="english").count()) )


# Finding Articles and Stopwords
db_articles = Article.objects.all()
print("Articles found : " + str(db_articles.count()) )
print("")

#db_articles = ['God is love love', 'OpenGL on the GPU is fast']
#db_articles2 = ['Today I can sing', 'Sometimes I get Lost in the forest']

clusterizer = CustomClusterizer(articles=db_articles)
clusters = clusterizer.multi_clusterize(iterations=1)

#ClusteringReport(date = str(datetime.now()), count = len(clusters), iterations = 10, nb_cluster = clusterizer.nb_clusters, cluster_list = clusters).save()

#from sklearn.externals import joblib
#joblib.dump(clusterizer.classifier, 'models/classifier.pkl')
#joblib.dump(clusterizer.vectorizer, 'models/vectorizer.pkl')





#print(len(cluster_labels))

print(" ")
print("Done clustering.")