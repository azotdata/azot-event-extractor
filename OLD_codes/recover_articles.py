#!/usr/local/python
################################################################################
#Author: Antsa Raharimanantsoa
#Description: Recover all rejected articles, restructure and store the document articles
#Creation_date: March 2017
################################################################################

from __future__ import print_function
import newspaper
from newspaper import *
from mongoengine import *
from document import NewArticle, ErrorDownload
from lib import *
from bson.objectid import ObjectId
import argparse

if connect(DATABASE_NAME):
    for elms in ErrorDownload.objects:
        a_url = elms.urls
        print('...', end = " ")
        article = Article(a_url, language=LANGUAGE, fetch_images=False, memoize_articles=False)
        article.build()
        article.download()
        article.parse()
        if article.title == '' or article.text == '':
            print(' ******** download error ******** ')
            pass
        else:
            if article.is_valid_url():
                ar = NewArticle()
                ar._id = ObjectId()
                ar.set_articles(article.title, article.text, a_url)
                ar.tokens = ','.join(tokenize_only(article.text))
                if article.publish_date:
                    ar.pub_date = str(article.publish_date[0].date())
                else:
                    ar.pub_date = str(article.publish_date)
                ar.save()
            ErrorDownload.objects(id=elms.id).delete()
