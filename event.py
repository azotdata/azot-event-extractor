from document import *
from mongoengine import *
from lib import *

connect(DATABASE_NAME)
test = NewArticle.objects(id=ObjectId('58dcfd60501ec210d1a89a73'))
print(test)
