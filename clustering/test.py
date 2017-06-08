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
db_articles = Article.objects.all()

#Evaluation cluster
#assessor = EvaluateClusterizer()
#evaluation = assessor.similarity_mesure(articles=db_articles)

#print("--------------------------------")
#for element,value in evaluation.iteritems():
#    print("-----------------------------------")
#    print(value)

# sortie : id cluster avec les mots importants pour chaque cluster (sauvegardé dans ClusterResumes)

#learning_set_size = int(round(len(tokenized)*0.80))
#print( "Learning Set Size : " + str(learning_set_size) )
#print( "Training Set Size : " + str((len(clusters) - learning_set_size)) )
#print(" ")
#
#learning_set = {}
#predict_set = {}
#index = 0
#
#print("Creating DataSets.")
#for key, cluster in tokenized.iteritems():
#    if index < learning_set_size:
#        learning_set[key] = cluster
#    else:
#        predict_set[key] = cluster
#    index += 1
#print("Done Creating DataSets.")

#print("------------------------------")
##le learning set ici est de type clé:keywords
#
#print("Learning Topics From DataSets.")
#labelised_wordbags, unclassified_clusters, known_tags = merger.process_manual(learning_set)
#print("Done Learning.")