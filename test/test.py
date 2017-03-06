#!/usr/local/python
import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from pymongo import MongoClient
from urls import Url
from article import NewArticle
from bson.objectid import ObjectId

cl = MongoClient()
db = cl.azotData
#connect('azotData')
#for elem in db.articles.find():
#    print(ObjectId(elem['_id']))
all_arts = dict((ObjectId(elem['_id']),elem['text']) for elem in db.articles.find())
#all_arts = dict((each_art._id,each_art.text) for each_art in  NewArticle.objects)
