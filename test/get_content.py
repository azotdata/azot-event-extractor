#!/usr/bin/python

#if connect('azotData'):
#    for arts in NewArticle.objects:
#        NewArticle.objects(arts.tokens) ).update(set__tokens__S=tokenize_only(arts.text))
#!/usr/local/python
import newspaper
from newspaper import Source
from newspaper import Article
from mongoengine import *
from article import TestArticle
from lib import *

filename = "urls.txt"
with open(filename, 'r') as f:
    data = f.read()  # Read the contents of the file into memory.\n",
        # Return a list of the lines, breaking at line boundaries
    myUrls = data.splitlines()

if connect('azotTest'):
    for art_url in myUrls:
	print('For art %s' %art_url)
        new_art = Article(art_url, language='en', fetch_images=False, memoize_articles=False)
        new_art.download()
        new_art.parse()

        art_obj = TestArticle()
        art_obj.title = new_art.title
        art_obj.text = new_art.text
        if new_art.publish_date:
            art_obj.pub_date = str(new_art.publish_date[0].date())
        else:
            art_obj.pub_date = str(new_art.publish_date)
        art_obj.source = art_url
        art_obj.tokens = tokenize_only(new_art.text)
        art_obj.save()
        print('...saved !')
    print('Articles saved to collection articles')


