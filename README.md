AZOT
====

Motivation
----------
AZOT is the fruit of mind connection of W3A's foundators, who want to do something innovating that consequently improving everyone's everyday life.
The main purpose is to simplify accessibility of datas, and express their values by analyzing them.

Synopsis
---------
This tool *classifies automatically* online newspaper articles to extract events from them, which will be organized in chronogical order.
There are steps to crete these events:
- 1 - collect in real time articles
- 2 - classify them according to their main topic
- 3 - Shape the events: name the cluster, detect date and location

Installation
------------

### Prerequisites: (These installations are for UBUNTU)
- First need to install [newspaper](https://github.com/codelucas/newspaper), documentation is [here](http://newspaper.readthedocs.io/en/latest/)

- [nltk](http://www.nltk.org/install.html) and [Corpora](http://www.nltk.org/nltk_data/)

- For the database, there are 2 possible choices:
        <br/>- [mongodb](https://docs.mongodb.com/manual/), with the plugin [mongoengine](http://mongoengine.org/) and [Robomongo](https://robomongo.org/) for viewing the datas.
        <br/>- [couchdb](http://couchdb.apache.org/). __It's mandatory to create the 4 views__ defined in the file [couchdb.views.json](couchdb.views.json) in the couchdb database. Creating view in Futon for couchdb is explained [here](https://blog.vicmetcalfe.com/2011/04/11/creating-views-in-couchdb-futon/)

- __Need these three packages to be installed for ssl issues with python 2.7 while exploring the sites:__
        <br/>- pyOpenSSL
        <br/>- ndg-httpsclient
        <br/>- pyasn1


Running the code
----------------
- Configure the system in [config.ini](config.ini):
        <br/> _The Database server_ : choose between __couchdb__ or __mongodb__ (uncomment the unused one)
        <br/>_The Database name_ : "azotdb" (Or whatever you want)
        <br/>_The path of stopwords files_ : by default [data] (data)
        <br/>_The language of the website source to be explored_ : set to "fr" by default
        <br/>_The path of log directory_

- Run the script for collecting datas in a neawspaper site with the following command: (Requires the source news (example: https://www.clicanoo.re) as parameter)
    > $ python collect\_newspaper\_article.py https://www.clicanoo.re

- To automatically generate the events'cluster, run the script for classification as follow:
    > $ python clustering_articles.py
