#!/usr/local/python
import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from article import NewArticle
from lib import *

sources = ['http://reunion.orange.fr/','http://www.zinfos974.com/','http://www.clicanoo.re/']

def get_all_urls(dbname=''):
    if connect(dbname):
        print('Successfully connected to Database!')
        all_urls = []
        for elements in NewArticle.objects:
            if elements.source != 'None':
                all_urls.append(elements.source)
    return all_urls

def fill_article_datas(source):
    sr = Source(source, verbose = True)
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

                art_obj = NewArticle()
                art_obj.title = new_art.title
                art_obj.text = new_art.text
                if new_art.publish_date:
                    art_obj.pub_date = str(new_art.publish_date[0].date())
                else:
                    art_obj.pub_date = str(new_art.publish_date)
                art_obj.source = art_url
		art_obj.tokens = ','.join(tokenize_only(new_art.text))
                art_obj.save()
		print('...saved !')
	print('Articles saved to collection articles')

for source in sources:
    fill_article_datas(source)
