from document import *
from mongoengine import *
from lib import *
from document import *

connect(DATABASE_NAME)

#test = NewArticle.objects(id=ObjectId('58e729d3501ec209f972832b'))
for each_cl in GroupCluster.objects:
    print('********titles per cluster*******')
    for each_elem in each_cl.article_lists:
        each_article = NewArticle.objects(id=ObjectId(each_elem))
        for elms in each_article:
            print(elms.source)
