AZOT
====

Motivation
----------
AZOT is the fruit of mind connection of W3A's foundators, who want to do something innovating that consequently improving everyone's everyday life.

Synopsis
---------
This tool aims to automatically extract events from unstructured datas in online newspaper texts.
The job is done in three steps:
1 - extract main content of articles (url source, title, content, publishing date, location) and store them
2 - classify them according to their subject
3 - populate the event base so that datas could be easily accessible to the interface

Installation
------------

### Prerequisites: (These installations are for UBUNTU)
- python-dev (sudo apt-get install python-dev)
- libxml2-dev and libxslt-dev for lxml (sudo apt-get install libxml2-dev libxslt-dev)
- libjpeg-dev, zlib1g-dev and libpng12-dev for images (sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev)
- nltk (we can read the full documentation http://www.nltk.org/install.html):
- To have Corpora of nltk : http://www.nltk.org/nltk_data/
    => we need stopwords, so we can directly go to point 68 (Stopwords) and download it (the french stopwords is also uploaded directly in this project, because of some improvement done)
- newspaper (pip install newspaper) (also *better* to get the one uploaded in this project)
- mongodb (sudo apt-get install mongodb)
- mongoengine (pip install mongoengine)

__Need these three packages to be installed for ssl issues with python 2.7 while exploring the sites:__
- pyOpenSSL
- ndg-httpsclient
- pyasn1

__For viewing the datas, use of Robomongo:__ (https://robomongo.org/)

Running the code
----------------

- Configure the system in config.ini:
        <br/>_The Database name_ : "azotData" (Or whatever you want)
        <br/>_The path of stopwords files_;
        <br/>_The language of the website source to be explored_ : set to "fr" by default

- Web scraping and storage of structured datas using newspaper: this is to collect, restructure and store the articles.
You must put the source news as parameter
.. code-block:: pycon
    > user@machine:~$ python collect_newspaper_article.py https://www.clicanoo.re
- Classification:
.. code-block:: pycon
    > user@machine:~$ python clustering.py

## Tests

## Contributors

## License

## TO DO
