#!/usr/bin/python
################################################################################
#Author: Antsa Raharimanantsoa
#Description: Collect, restructure and store the document articles
#Creation_date: March 2017
################################################################################

from newspaper import *
from mongoengine import *
from document import NewArticle, ErrorDownload
from lib import *
from bson.objectid import ObjectId
import argparse
import logging
from datetime import datetime

log_name = datetime.now().strftime("%Y%m%d_%H%M")
logging.basicConfig(filename='log/collect/' + log_name + '.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%d-%m-%Y %I:%M:%S %p')

#get the url parameter when the command line is entered
class EscapeNamespace():
    pass
escape = EscapeNamespace()
parser = argparse.ArgumentParser(description='Process newspaper url sources')
parser.add_argument('sources',help='permits the scrapping of the url source in argument ',nargs=1)
argum = parser.parse_args(namespace=escape)

source = escape.sources
sr = Source(source[0], verbose = True)
sr.clean_memo_cache()
sr.build()
print('...build done!')
logging.info('...build done!')

if connect(DATABASE_NAME):
    print('collecting article ...')
    logging.info('collecting article')
    for art_url in sr.article_urls():
        if art_url not in [elms.source for elms in NewArticle.objects]:
            http_resp = get_http_response(art_url)
            logging.info('HTTP response %s' %http_resp)
            if http_resp is None:
                logging.info('Request OK!')
                new_art = Article(art_url, language=LANGUAGE, fetch_images=False, memoize_articles=False)
                new_art.download()
                new_art.parse()
                logging.info('Extraction OK!')
                if new_art.title == '' or new_art.text == '':
                    print(' ******** download error ******** ')
                    logging.warning('Download error!!')
                    logging.error('Could not download %s' %art_url)
                    err_dl = ErrorDownload()
                    err_dl.urls = art_url
                    err_dl.save()
                    continue
                else:
                    if new_art.title not in [elms.title for elms in NewArticle.objects]:
                        logging.info('Storing the structured datas')
                        art_obj = NewArticle()
                        art_obj._id = ObjectId()
                        art_obj.set_articles(new_art.title,new_art.text,art_url)
                        art_obj.tokens = ','.join(tokenize_only(new_art.text))
                        if new_art.publish_date:
                            art_obj.pub_date = str(new_art.publish_date[0].date())
                        else:
                            art_obj.pub_date = str(new_art.publish_date)
                        art_obj.save()
                        logging.info('Datas successfully saved for the article whose link is %s! NEXT?' %art_url)
            else:
                pass

print('Articles saved to collection articles')
logging.info('Articles saved for this source')
