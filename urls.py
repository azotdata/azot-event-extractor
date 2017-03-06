#!usr/bin/python

from mongoengine import *

class Url(Document):
    brand = StringField(required=True)
    url = StringField(required=True)
    meta = {'collection': 'urlSource','strict':False}
