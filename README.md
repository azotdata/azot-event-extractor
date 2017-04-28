
## Motivation
AZOT is the fruit of mind connection of W3A's foundators, who want to do something innovating that consequently improving everyone's everyday life.

## Synopsis
This tool aims to automatically extract events from unstructured datas in online newspaper texts.
The job is done in three steps:
1 - extract main content of articles (url source, title, content, publishing date, location) and store them
2 - classify them according to their subject
3 - populate the event base so that datas could be easily accessible to the interface

## Installation

### Prerequisites: (These installations are for UBUNTU)
- python-dev (sudo apt-get install python-dev)
- libxml2-dev et libxslt-dev pour lxml (sudo apt-get install libxml2-dev libxslt-dev)
- libjpeg-dev, zlib1g-dev et libpng12-dev pour les images (sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev)
- nltk (we can read the full documentation http://www.nltk.org/install.html):
- for rake module, it's better to clone here https://github.com/zelandiya/RAKE-tutorial
- To have Corpora of nltk : http://www.nltk.org/nltk_data/
    => we need stopwords, so we can directly go to point 68 (Stopwords) and download it (the frech stopwords is also uploaded directly in this project, because of some improvement done)
- newspaper (pip install newspaper) (also better to get the one uploaded in this project)
- mongodb (sudo apt-get install mongodb)
- mongoengine (pip install mongoengine)
- need to install the newspaper uploaded here because of some changes

### Need this three packages to be installed for processing french language:
    - pyOpenSSL
    - ndg-httpsclient
    - pyasn1

### For viewing the datas, use of mongs
(https://github.com/whit537/mongs)  

## Exploring and Running the code

- Configure the system, by editing the variables at lib.py:
        <br/>_The Database name_
        <br/>DATABASE_NAME = 'azotData'
        <br/>_The language of the website source to be explored_
        <br/>LANGUAGE = 'fr'
        <br/>_Name of the collection containing the structured datas of the articles_
        <br/>ARTICLE_COLLECTION = 'articles'
        <br/>_Name of the collection containing the clusters_
        <br/>CLUSTER_COLLECTION = 'clusters'
        <br/>_Name of the collection containing the article urls that could not be downloaded_
        <br/>BAD\_URL\_COLLECTION = 'download_error'
        <br/>\_\_version\_\_ = '0.1'

- Extraction of main content:
        <br/> => run python collect\_article.py _source URL_ (example: https://www.clicanoo.re) : this is to collect, restructure and store the articles.
- Classification: yet to be improved
        <br/> => run clustering.py
- Generate the Event collection, [FROM NOW: collecting the title and the urls of all articles in clusters, no title, date or location for the event yet]
        <br/> => run event.py

## Tests
The file __Test.ipynb__ is very useful for a punctual test.
<br/> Installation of ipython notebook is necessary for this.

## Contributors

## License

## TO DO
