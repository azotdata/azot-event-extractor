#!/usr/local/python
################################################################################
#Author: Antsa Raharimanantsoa
#Description: Collect, restructure and store the document articles
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

#get the url parameter when the command line is entered
class EscapeNamespace():
    pass
escape = EscapeNamespace()
parser = argparse.ArgumentParser(description='Process newspaper url sources')
parser.add_argument('sources',help='permits the scrapping of the url source in argument ',nargs=1)
argum = parser.parse_args(namespace=escape)
source = escape.sources

sr = Source(source[0])#, verbose = True)
sr.clean_memo_cache()
sr.build()
print('...build done!')

coll_urls = get_art_urls(DATABASE_NAME)

if connect(DATABASE_NAME):
    print('collecting article ...')
    for art_url in sr.article_urls():
        if art_url not in coll_urls:
            http_resp = get_http_response(art_url)
            if http_resp is None:
                print('...', end = " ")
                new_art = Article(art_url, language=LANGUAGE, fetch_images=False, memoize_articles=False)
                new_art.download()
                new_art.parse()
                if new_art.title == '' or new_art.text == '':
                    print(' ******** download error ******** ')
                    err_dl = ErrorDownload()
                    err_dl.urls = art_url
                    err_dl.save()
                    continue
                else:
                    if new_art.is_valid_url():
                        art_obj = NewArticle()
                        art_obj._id = ObjectId()
                        art_obj.set_articles(new_art.title,new_art.text,art_url)
                        art_obj.tokens = ','.join(tokenize_only(new_art.text))
                        if new_art.publish_date:
                            art_obj.pub_date = str(new_art.publish_date[0].date())
                        else:
                            art_obj.pub_date = str(new_art.publish_date)
                        art_obj.save()
            else:
                pass

print('Articles saved to collection articles')
