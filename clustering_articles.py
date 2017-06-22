# -*- coding: utf-8 -*-
""""
This script is run for proceeding to the classification of articles.
Need to initialize iteration number (must be 2 or 3 only). 2 by default
"""

from __future__ import unicode_literals
from clustering import *

print("Starting Clustering.")
clusterizer = CustomClusterizer()
clusters = clusterizer.multi_clusterize(iterations=2)

print("Starting Tokenization and Save clusters")
merger = CustomMerger()
merger.tokenize_clusters(clusters)
print("Done Tokenization.")
print(" ")
print("-------------------------------")
