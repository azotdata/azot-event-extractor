"""
This script contains class definition of the scraping and storage of newspapers
"""

from newspaper import Source as NpSource
from newspaper import Article as NpArticle
from bson.objectid import ObjectId
import logging

from models import *
from utils import get_http_response

class CollectUrls():
    """
    Parent class that can be used elsewhere.
    Gets all articles urls stored in the database
    """
    def __init__(self):
        pass

    # This function extracts all urls
    @staticmethod
    def get_all_urls():
        articles_urls = [document.source for document in Article.objects]
        return articles_urls


class CollectArticle(CollectUrls):
    """
    Class for articles extraction by source news.
    Scraps and stores them in database
    """
    def __init__(self):
        pass

    # method called while instantiate CollectArticle object in order to scrap a source news
    def extract_from_source(self,source,lang='fr'):
        news = NpSource(source, verbose = True)
        news.clean_memo_cache()
        news.build()
        logging.info('...build done!')

        for url in news.article_urls():
            if self.not_duplicate_url(url):
                if self.is_responding(url):
                    article = self.extract_articles(url,lang)
                    self.store_structured_article(article)

    # calls newspaper Article class to scrap an article
    @staticmethod
    def extract_articles(url,lang):
        article = NpArticle(url,lang,fetch_images=False,memoize_articles=False)
        article.download()
        article.parse()
        return article

    # checks if the web page designed by its link is still online and accessible
    @staticmethod
    def is_responding(url):
        http_resp = get_http_response(url)
        logging.info('HTTP response %s' % http_resp)
        if http_resp is None:
            return True

    # checks if the article already exists in our database
    def not_duplicate_url(self,url):
        all_urls = self.get_all_urls()
        if url not in all_urls:
            return True

    # stores the article datas in Article collection
    @staticmethod
    def store_structured_article(article):
        structured_article=Article()
        structured_article.id=ObjectId()
        structured_article.set_article(article)
        structured_article.save()
        logging.info('Datas successfully saved for the article whose link is %s! NEXT?' % article.url)
