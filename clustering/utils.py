# -*- coding: utf-8 -*-
""""This script contains common independent functions that are used during the project"""

from __future__ import unicode_literals
from models import *

import os
import logging
from datetime import datetime

import nltk
from sklearn import cluster
from sklearn.feature_extraction.text import TfidfVectorizer
from urllib2 import Request, urlopen, URLError
from cookielib import CookieJar as cj

__version__ = '0.1'

# Check the response of the http request
def get_http_response(url):
    det = {'User-Agent': 'azot-extractor/%s' % __version__,
            'cookies': cj(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = Request(url.encode("UTF-8"), headers = det)
    try:
        response = urlopen(req)
    except URLError as e:
        if hasattr(e, 'code'):
            return e.code
    return None

# Store the logs when running the program
def write_logs(dirname):
    log_name = datetime.now().strftime("%Y%m%d_%H%M")
    try:
        os.makedirs(dirname)
    except OSError:
        if os.path.exists(dirname):
            pass
        else:
            raise
    logging.basicConfig(filename=dirname + '/' + log_name + '.log',
                        level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%d-%m-%Y %I:%M:%S %p')
    return None