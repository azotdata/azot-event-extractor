#!/usr/local/python
import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from article import NewArticle
from lib import *
from bson.objectid import ObjectId
import argparse

#functions for extraction process
def get_all_urls(dbname=''):
    if connect(dbname):
        print('Successfully connected to Database!')
        all_urls = []
        for elements in NewArticle.objects:
            if elements.source != 'None':
                all_urls.append(elements.source)
    return all_urls

def fill_article_datas(link):
    sr = Source(link, verbose = True)
    sr.clean_memo_cache()
    sr.build()
    print('...build done!')

    coll_urls = get_all_urls('azotData')
    if connect('azotData'):
        for art_url in sr.article_urls():
            if art_url not in coll_urls:
                new_art = Article(art_url, language='fr', fetch_images=False, memoize_articles=False)
                new_art.download()
                new_art.parse()

                if new_art.is_valid_url():
                    art_obj = NewArticle()
                    art_obj._id = ObjectId()
                    art_obj.title = new_art.title
                    print(art_obj.title)
                    art_obj.text = new_art.text
                    print(art_obj.text)
                    art_obj.tokens = ','.join(tokenize_only(new_art.text))
                    print(art_obj.tokens)
                    if new_art.publish_date:
                        art_obj.pub_date = str(new_art.publish_date[0].date())
                    else:
                        art_obj.pub_date = str(new_art.publish_date)
                    art_obj.source = art_url
                    art_obj.save()
		print('...saved !')
	print('Articles saved to collection articles')

#get the url parameter when the command line is entered
class EscapeNamespace():
    pass
escape = EscapeNamespace()
parser = argparse.ArgumentParser(description='Process newspaper url sources')
parser.add_argument('sources',help='permits the scrapping of the url source in argument ',nargs=1)
argum = parser.parse_args(namespace=escape)
source = escape.sources

#Execute the etraction
fill_article_datas(source[0])
