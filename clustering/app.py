# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from mongoengine import *
from os import listdir
from os.path import isfile, join
from ConfigParser import SafeConfigParser


from processing import *

# ----- Start generating Config File ----
# --- Code permettant de générer un fichier ini si config.ini n'est pas présent dans le dossier
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

# Initialisation de la connexion à la BDD
connect(config.get('database', 'name'))



# ===== Phase 0 : Import des Stopwords =====
# Les Stopwords sont importés dans la base depuis les fichiers si ça n'a jamais été fait.
# Sinon, ils sont juste lus depuis Mongo
print(" ===== Phase 0 : Stopwords ===== " )

stopwords_path = config.get('stopwords', 'folder_path')
if Stopword.objects.count() == 0:
    print("No stopwords found. Importing from files.")

    lang_files = [f for f in listdir(stopwords_path) if isfile(join(stopwords_path, f))]

    # Parsing de chaque fichier
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

print("Loading Stopwords... " )
print("French stopwords found : " + str(Stopword.objects(lang="french").count()) )
print("English stopwords found : " + str(Stopword.objects(lang="english").count()) )
print(" ")



# ===== Phase 1 : Chargement des articles =====
# Les Articles sont chargés depuis la base de données
# Cette phase pourrait être améliorée pour proposer plus de finesse dans la façon dont les articles sont chargés, si nécessaire.
print(" ===== Phase 1 : Articles ===== " )

db_articles = Article.objects.all()
print("Articles found : " + str(db_articles.count()) )
print(" ")



# ===== Phase 2 : Clusterisation des articles =====
# Les Articles sont regroupés en plusieurs petits clusters d'articles.
# L'algorithme fonctionne de manière itérative. Il utilise KMeans pour créer X clusters.
# Puis répète la même opération sur chaque cluster obtenu. Le nombre d'itérations peut être paramétré.
print(" ===== Phase 2 : Clusterisation des articles ===== " )

print("Starting Clustering.")
clusterizer = CustomClusterizer(articles=db_articles)
clusters = clusterizer.multi_clusterize(iterations=5)
print("Done Clustering.")

print( "Clusters Found : " + str(len(clusters)) )



# ===== Phase 3 : Regroupement des clusters =====
# Les clusters sont tokenizés pour déterminer les termes les plus importants.
# Ensuite, une partie des clusters générés est utilisée pour l'apprentissage et l'autre pour les prédictions.
# Le traitement d'apprentissage est manuel pour le moment
print(" ===== Phase 3 : Regroupement des clusters ===== " )

print("Starting Tokenization.")
merger = CustomMerger()
tokenized  = merger.tokenize_clusters(clusters)
print("Done Tokenization.")
print(" ")

learning_set_size = int(round(len(tokenized)*0.80))
print( "Learning Set Size : " + str(learning_set_size) )
print( "Training Set Size : " + str((len(clusters) - learning_set_size)) )
print(" ")

learning_set = {}
predict_set = {}
index = 0

print("Creating DataSets.")
for key, cluster in tokenized.iteritems():
    if index < learning_set_size:
        learning_set[key] = cluster
    else:
        predict_set[key] = cluster
    index += 1
print("Done Creating DataSets.")

print("Learning Topics From DataSets.")
labelised_wordbags, unclassified_clusters, known_tags = merger.process_manual(learning_set)
print("Done Learning.")



# ===== Phase 4 : Sauvegarde des topics =====
# Les topics saisis par l'utilisateur lors de l'apprentissage et les mots associés sont enregistrés
print(" ===== Phase 4 : Sauvegarde des topics ===== " )

print("Starting Saving Topics.")
topic_handler = TopicHandler()
topic_handler.save_words(labelised_wordbags)
print("Done Saving Topics.")



# ===== Phase 5 : Prédictions =====
# On essaye de prédire le topic des clusters qui n'ont pas été utilisés dans l'apprentissage.
print(" ===== Phase 5 : Prédictions ===== " )

print("Starting Predictions.")
for key, cluster in predict_set.iteritems():
    topic, topic_list = topic_handler.identify_wordbag(cluster.keys())

    print("Cluster Words : ")
    print( cluster.keys() )
    print("Predicted Topic : ")
    print(topic)
    print("Topic Prediction Details : ")
    print(topic_list)
    print('  ')
print("Done Predictions.")


print(" ===== Done Processing ===== ")
