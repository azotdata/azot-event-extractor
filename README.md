## Synopsis

This tool aims to automatically extract events from unstructured datas in online newspaper texts.
The job is done in three steps:
1 - extract main content of articles (url source, title, content, publishing date, location) and store them
2 - classify them according to their subject
3 - populate the event base so that datas could be easily accessible to the interface

## Code Example

- Extraction of main content: mainly done in "collect_articles.py" file using Article and Url classes, including storage to the database too.
- Classification: use of MeanShift algorithm and storage of the result, by launching the clustering.py script
- Generate the Event collection, which is most useful for the interface (to be done)

## Motivation

AZOT is the fruit of mind connection of W3A's foundators, who want to do something innovating that consequently improving everyone's everyday life.

## Installation
Prerequisites: (These installations are for UBUNTU)
- python-dev (sudo apt-get install python-dev)
- libxml2-dev et libxslt-dev pour lxml (sudo apt-get install libxml2-dev libxslt-dev)
- libjpeg-dev, zlib1g-dev et libpng12-dev pour les images (sudo apt-get install libjpeg-dev zlib1g-dev libpng12-dev)
- nltk (we can read the full documentation http://www.nltk.org/install.html)
- To have Corpora of nltk : http://www.nltk.org/nltk_data/
    => we need stopwords, so we can directly go to point 68 (Stopwords) and download it
- newspaper (pip install newspaper)
- mongodb (sudo apt-get install mongodb)
- mongoengine (pip install mongoengine)

For viewing the datas, use mongs
(https://github.com/whit537/mongs)  

## API Reference

## Tests

## Contributors

## License
