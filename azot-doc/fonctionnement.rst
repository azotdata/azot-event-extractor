


Fonctionnement d’AZOT
=====================



Comment l’installer?
~~~~~~~~~~~~~~~~~~~~
Les prérequis indispensables sont les suivants:

+ `newspaper`_ (pour le web scraping)
+ `nltk`_(pour le traitement des textes)
+ système de gestion de base de données No-SQL:

    + `mongodb`_, il faut aussi installer `mongoengine`_
    + `couchdb`_. Il nécessite le plugin `couchdbpython`_



Ceci étant fait, le projet peut être cloné sur `ce lien`_.

Avant toute exécution, il faut s'assurer que le fichier de
configuration *config.ini* continne les bonnes informations:


+ nom du système de gestion de base de données adopté (mongodb ou
  couchdb, **commenter celui qui n'est pas utilisé**
+ nom de la base de donnée
+ les chemins de log et de stopwords sont par défaut ceux avec le
  projet.




Comment le lancer?
~~~~~~~~~~~~~~~~~~


+ La collecte est lancée autant de fois que possible en background,
  afin d’avoir les informations en temps réel émises par les sites
  scrapés  Il faut donner en paramètre **le site à parcourir** (exemple:
  https://www.lemondefr)

::

    python collect_newspaper_article.py https://www.lemondefr


+ Pour le clustering, il est à lancer quelque fois par semainepour
  maintenir l'integrité des évènements.

::

    python clustering_article.py






Table des Matières
~~~~~~~~~~~~~~~~~~


+ `Introduction`_
+ `Premier aperçu d'Azot`_
+ `Structure du projet`_
+ Fonctionnement d’AZOT
+ `Contribuons au projet`_




Related Topics
~~~~~~~~~~~~~~


+ `Documentation overview`_



2017, w3a. | Powered by `Sphinx 1.6.2`_ & `Alabaster 0.7.10`_
.. _Alabaster 0.7.10: https://github.com/bitprophet/alabaster
.. _Documentation overview: index.html
.. _mongoengine: http://mongoengine.org/
.. _nltk: http://www.nltk.org/
.. _Premier aperçu d'Azot: genindex.html
.. _Sphinx 1.6.2: http://sphinx-doc.org/
.. _Contribuons au projet: etat-projet.html
.. _mongodb: https://docs.mongodb.com/manual/tutorial/getting-started/
.. _Structure du projet: structure-code.html
.. _ce lien: https://github.com/azotdata/azot-event-extractor.git
.. _couchdb: http://couchdb.apache.org/
.. _newspaper: https://github.com/antsafi/newspaper.git
.. _python: https://pythonhosted.org/CouchDB/


