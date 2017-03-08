#!/usr/bin/python

import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from article import TestArticle
from lib import *

print('Starting the update...')
if connect('azotTest'):
    for elem in TestArticle.objects:
	TestArticle.objects(source=elem.source).update(tokens=tokenize_only(elem.text))
	print('update done for this!')
