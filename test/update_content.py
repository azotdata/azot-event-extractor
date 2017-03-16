#!/usr/bin/python
import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from article import TestArticle
from lib import *
from bson.objectid import ObjectId

print('Starting the update...')
if connect('azotTest'):
    for elem in TestArticle.objects:
        elem.update(set__newfield='value')
	print('update done for this!')
