"""
This script contains class definition of the scraping and storage of newspapers
"""

import logging
from newspaper import Article as NpArticle
from newspaper import Source as NpSource
from utils import *

if DB_SERVER == 'couchdb':
    from db_couchdb import *
elif DB_SERVER == 'mongodb':
    from db_mongodb import *

write_logs(DIRNAME)

class CollectArticle():
    """
    Class for articles extraction by source news.
    Scraps and stores them in database
    """
    def __init__(self):
        self.lang = LANG
        self.connecting = Connection(DB_SERVER)
        self.connecting.connect()

    # method called while instantiate CollectArticle object in order to scrap a source news
    def extract_from_source(self,source):
        news = NpSource(source, verbose = True)
        news.clean_memo_cache()
        news.build()
        logging.info('...build done!')
        for url in news.article_urls():
            if self.is_available_url(url):
                article = self._extract_articles(url)
                if self.is_available_article(article):
                    self._store_article(article)

    # calls newspaper Article class to scrap an article
    def _extract_articles(self,url):
        article = NpArticle(url,self.lang,fetch_images=False,memoize_articles=False)
        article.download()
        article.parse()
        return article

    # Check the link if available or not
    def is_available_url(self,url):
        structured_article = Article()
        if structured_article.check_article_url(url):
            # defined in utils.py, and checks whether the page is available or not found
            http_resp = get_http_response(url)
            logging.info('HTTP response %s' % http_resp)
            if http_resp:
                return True
        del structured_article

    @staticmethod
    def is_available_article(article):
        if article.text != "":
            if "LINFO" not in article.text:
                return True

    # stores the article datas in Article collection
    @staticmethod
    def _store_article(article):
        structured_article = Article()
        structured_article.save_article(article)
        logging.info('Datas successfully saved for the article whose link is %s! NEXT?' % article.url)
        del structured_article
