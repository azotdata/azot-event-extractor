AZOT
====

Motivation
----------
AZOT is the fruit of mind connection of W3A's foundators, who want to do something innovating that consequently improving everyone's everyday life.

Synopsis
---------
This tool aims to *automatically extract events* from unstructured datas in online newspaper texts.
The job is done in three steps:
1 - extract main content of articles (url source, title, content, publishing date, location) and store them
2 - classify them according to their subject
3 - populate the event base so that datas could be easily accessible to the interface

Installation
------------

### Prerequisites: (These installations are for UBUNTU)
- First need to install [newspaper](https://github.com/codelucas/newspaper), documentation is [here](http://newspaper.readthedocs.io/en/latest/)

- [nltk](http://www.nltk.org/install.html) and [Corpora](http://www.nltk.org/nltk_data/)

- [mongodb](https://docs.mongodb.com/manual/) as Database and need to install the plugin [mongoengine](http://mongoengine.org/)

__Need these three packages to be installed for ssl issues with python 2.7 while exploring the sites:__
- pyOpenSSL
- ndg-httpsclient
- pyasn1

__For viewing the datas, use of__ [Robomongo](https://robomongo.org/)

Running the code
----------------
- Codes relative to the automatic event extraction are under [clustering](clustering/) folder
- Configure the system in [config.ini](clustering/config.ini):
        <br/>_The Database name_ : "azotData" (Or whatever you want)
        <br/>_The path of stopwords files_;
        <br/>_The language of the website source to be explored_ : set to "fr" by default

- Web scraping uses [newspaper](https://github.com/codelucas/newspaper) this is to collect and restructure the articles. They are then stored.
- Requires the source news (example: https://www.clicanoo.re) as parameter
    > $ python collect_newspaper_article.py https://www.clicanoo.re
- Can also be imported as module:
```python
from scraping_newspapers import CollectArticle
collect_article = CollectArticle()
collect_article.extract_from_source('https://www.clicanoo.re','fr')
```
- Classification:
    > $ python clustering.py
- Also can be called as module:
```python
from clustering import CustomClusterizer
clusterizer = CustomClusterizer(articles)
clusters = clusterizer.multi_clusterize(iterations=2)
```

## Tests

## Contributors

## License
