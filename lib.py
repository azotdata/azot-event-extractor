#!/usr/bin/python

###############################################################################################################################################################
#Author: Antsa Raharimanantsoa
#Description: librairies for function mostly used
#Dependencies: Requires newspaper, nltk, sickit-learn, pandas to be installed
# git clone https://github.com/codelucas/newspaper for newspaper
#Creation_date: 24/02/2017
##############################################################################################################################################################

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

def keywords(rawtext, n=0):
    #from newspaper
    import nltk

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

def get_content_article():
    #from mongoengine import *
    from article import NewArticle
    from pymongo import MongoClient
    from bson.objectid import ObjectId

    cl = MongoClient()
    db = cl.azotTest
    all_arts = dict((ObjectId(elem['_id']),elem['text']) for elem in db.testarticles.find())

    return all_arts
