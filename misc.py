# -*- coding: utf-8 -*-
from newspaper import Article as NpArticle
from newspaper import Source as NpSource
from utils import *

if DB_SERVER == 'couchdb':
    from db_couchdb import *
elif DB_SERVER == 'mongodb':
    from db_mongodb import *

url = "https://www.clicanoo.re/AFP/Article/2017/06/20/Colombie-les-Farc-dans-la-derniere-ligne-droite-du-desarmement_475376#disqus_thread"

art = ClusteringResume()

print(list(res))