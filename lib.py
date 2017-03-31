# -*- coding: utf-8 -*-
###############################################################################################################################################################
#Author: Antsa Raharimanantsoa
#Description: librairies for variables and functions mostly used
#Creation_date: Feb-March 2017
##############################################################################################################################################################
""" Below are global variables that are used frequently"""
DATABASE_NAME = 'azotData'
LANGUAGE = 'fr'
ARTICLE_COLLECTION = 'articles'
CLUSTER_COLLECTION = 'clusters'
BAD_URL_COLLECTION = 'download_error'
__version__ = '0.1'

"""Below are some functions that may be used frequently"""
def tokenize_and_stem(text):
    import nltk
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords += nltk.corpus.stopwords.words('french')

    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out stopwords
    for token in tokens:
        if token not in stopwords:
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    import nltk
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords += nltk.corpus.stopwords.words('french')

    tokens = [word for word in nltk.word_tokenize(text) if word.isalpha()]
    filtered_tokens = []
    # filter out stopwords
    for token in tokens:
        if token not in stopwords:
            filtered_tokens.append(token)
    return filtered_tokens

"""This function is a customization of the keywords from newspaper
    It returns the n most repeated words per a collection of words"""
def keywords(rawtext, n=0):
    #from newspaper
    import nltk
    from nltk import word_tokenize

    stopwords = nltk.corpus.stopwords.words('english')
    stopwords += nltk.corpus.stopwords.words('french')
    NUM_KEYWORDS = n
    if rawtext:
        text = rawtext.split(',')
        num_words = len(text)
        text = [x for x in text if x not in stopwords]

        freq = {}
        for word in text:
            if word in freq:
                freq[word] += 1
            else:
                freq[word] = 1
        min_size = min(NUM_KEYWORDS, len(freq))
        keywords = sorted(freq.items(),
                          key=lambda x: (x[1], x[0]),
                          reverse=True)
        keywords = keywords[:min_size]
        keywords = dict((x, y) for x, y in keywords)

        for k in keywords:
            articleScore = keywords[k] * 1.0 / max(num_words, 1)
            keywords[k] = articleScore * 1.5 + 1
        return dict(keywords)
    else:
        return dict()

"""This function returns a dict with the id of the article and the text, useful for the clustering"""
def get_content_article():
    from mongoengine import connect
    from document import NewArticle
    if connect(DATABASE_NAME):
        all_arts = dict((elem.id,elem.text) for elem in NewArticle.objects)
    return all_arts

"""This function returns all the article urls already contained in the database"""
def get_art_urls(dbname=''):
    from mongoengine import connect
    from document import NewArticle

    if connect(dbname):
        print('Successfully connected to Database!')
        all_urls = []
        for elements in NewArticle.objects:
            if elements.source != 'None':
                all_urls.append(elements.source)
    return all_urls

def get_err_urls(dbname=''):
    from mongoengine import connect
    from document import ErrorDownload

    if connect(dbname):
        print('Successfully connected to Database!')
        all_urls = []
        for elements in ErrorDownload.objects:
            if elements.urls != 'None':
                if elements.urls not in all_urls:
                    all_urls.append(elements.urls)
                else:
                    pass
    return all_urls

"""This function checks the response of the http request"""
def get_http_response(url):
    from urllib2 import Request, urlopen, URLError
    from cookielib import CookieJar as cj

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
