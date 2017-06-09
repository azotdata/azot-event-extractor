"""
This script makes a graphic representation of articles' number for each cluster
"""
from __future__ import unicode_literals

from mongoengine import *
from ConfigParser import SafeConfigParser
import matplotlib.pyplot as plt
from processing import *
from operator import itemgetter
from itertools import groupby

# Reading Config file
config = SafeConfigParser()
config.read('config.ini')

# Initialisation de la connexion  a la BDD
connect(config.get('database', 'name'))

table = []
for article in Article.objects:
    table.append((article.title,article.num_cluster))

sorted_table = sorted(table, key=itemgetter(1))
table = groupby(sorted_table, key=itemgetter(1))
article_table = [{'cluster':k,
                    'title':[elms1 for (elms1,elms2) in v]} for k, v in table]
x = [cluster for cluster,title in enumerate(article_table)]
y = [len(article_table[ind]['title']) for ind,value in enumerate(article_table)]
#
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(x, y)
plt.show()

#print(y)
