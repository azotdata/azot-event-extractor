# -*- coding: utf-8 -*-
""""This script contains common independent functions that are used during the project"""

from __future__ import unicode_literals
import os
from os import listdir
from os.path import isfile, join
import logging
from datetime import datetime
from urllib2 import Request, urlopen, URLError
from cookielib import CookieJar as cj

from ConfigParser import SafeConfigParser

# Reading Config file
config = SafeConfigParser()
config.read('config.ini')

# Get parameters
LANG = config.get('language', 'language')
SW_PATH = config.get('stopwords', 'folder_path')
DB_SERVER = config.get('server', 'server_name')
DB_NAME = config.get('database', 'name')
DIRNAME = config.get('log_path','folder_path')

__version__ = '0.1'

# Check the response of the http request
def get_http_response(url):
    headers = {'User-Agent': 'azot-extractor/%s' % __version__,
            'cookies': cj(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    req = Request(url.encode('utf-8'), headers = headers)
    try:
        urlopen(req)
    except URLError as e:
        if hasattr(e, 'code'):
            return e.code
    except UnicodeDecodeError as e1:
        if hasattr(e1, 'code'):
            logging.debug('Encoding error with url:',url)
            return e1.code

    return True

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

def stopwords_list(sw_path):
    lang_files = [f for f in listdir(sw_path) if isfile(join(sw_path, f))]
    # Parsing de chaque fichier
    word_list = {}
    for lang in lang_files:
        word_list[lang] = []
        with open(sw_path + "/" + lang) as f:
            print("Inserting '" + lang + "' stopwords into collection.")

            word_string = f.read().decode('utf-8')
            #word_string = f.read()
            #words_list = [word.replace("\r", "").lower().encode('utf-8') for word in word_string.split("\n") if word != "".encode('utf-8')]
            words_list = [word.replace("\r", "").lower() for word in word_string.split("\n")]
        for word in words_list:
            word_list[lang].append(word)
            #word_list[lang] += word
    return word_list