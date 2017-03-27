#!/usr/bin/python

from article import NewArticle
#Constitute the Event base
for mem in GroupCluster.objects:
    kwds = mem.keywords
    newA = dict(sorted(kwds.iteritems(), key=itemgetter(1), reverse=True)[:5])
    #sorted(kwds, key=kwds.get, reverse=True)[:5]
    print('-------------------')
    #import heapq
    #heapq.nlargest(5, A, key=A.get)
