#!/usr/bin/python
import newspaper
from newspaper import Article
art_url = 'http://www.linfo.re/ocean-indien/madagascar/713801-passage-d-enawo-a-madagascar-50-morts-et-296-125-sinistres-selon-un-nouveau-bilan'
tableau = {'title':'','text':'','date':''}
new_art = Article(art_url, fetch_images=False, memoize_articles=False)
new_art.download()
new_art.parse()
tableau['title'] = new_art.title
tableau['text'] = new_art.text
tableau['date'] = ''

print(tableau)
