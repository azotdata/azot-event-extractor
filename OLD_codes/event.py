from document import *
from mongoengine import *
from lib import *
from document import *

if connect(DATABASE_NAME):
    #test = NewArticle.objects(id=ObjectId('58e729d3501ec209f972832b'))
    Event.objects().delete()
    for each_cl in GroupCluster.objects:
        titles = []
        sources = []
        event = Event()
        for each_elem in each_cl.article_lists:
            each_article = NewArticle.objects(id=ObjectId(each_elem))
            for elms in each_article:
                titles.append(elms.title)
                sources.append(elms.source)
        event.titles_list = titles
        event.sources_list = sources
        event.save()
