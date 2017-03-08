#!/usr/local/python
import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from article import NewArticle
from lib import *

if connect('azotData'):
    for elem in NewArticle.objects:
        NewArticle.objects(source=elem.source).update(tokens=tokenize_only(elem.text))
        print('update done for this!')

