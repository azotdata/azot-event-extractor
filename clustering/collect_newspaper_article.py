# -*- coding: utf-8 -*-
""""
The script which scraps newspaper. Needs the source of the newspaper as parameter.
It uses the CollectArticle class 
"""

from __future__ import unicode_literals

from mongoengine import connect
from ConfigParser import SafeConfigParser
import argparse
from utils import write_logs
from scraping_newspapers import *

# Configure log directory and file
dirname = "log/collect_articles"
write_logs(dirname)

# Reading Config file
config = SafeConfigParser()
config.read('config.ini')

# Connect to the DB
connect(config.get('database', 'name'))

# Get default language
lang = config.get('language', 'language')

# Get parameter from script
class EscapeNamespace():
    pass
escape = EscapeNamespace()
parser = argparse.ArgumentParser(description='Process newspaper url sources')
parser.add_argument('sources',help='Permits the scrapping of the url source in argument ',nargs=1)
argument = parser.parse_args(namespace=escape)
source = escape.sources

# Collect articles from source given in argument
collect_article = CollectArticle()
collect_article.extract_from_source(source[0],lang)