


Structure du projet
===================

Pour l’instant, Azot s’intéresse surtout aux articles de journaux,
dont les informations sont quasiinexploitées. Il est basé sur une
intelligence artificielle :


+ qui restructure les articles des presses en ligne en données
  manipulables
+ qui classifie automatiquement ces article selon leur sujet


Le but est de synthétiser les informations contenues dans les journaux
pour faire émerger leur potentiel.
Pour ce faire, l'équipe a adopté l'approche par la classification
automatique en mode non-supervisé des textes ainsi recueillis.

L'intégralité d'Azot est développé en **Python**

Le traitement comprend donc deux phases:



Phase de collecte de données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~


+ Effectué via le script *collect_newspaper_article.py*
+ Il fait du “ **web scraping**”, puis stocke les données
  restructurées dans la base de données.
+ L’extraction des informations se fait avec l’outil `newspaper`_,
  dont l’utilisation et les fonctionnalités sont explicitées dans la`
  documentation`_

::

    >>> import newspaper
                              
    >>> ...class CollectArticle(ArticleManager):
                              
    >>> ... def extract_from_source(self, url):
                              
    >>> ... /* ... */
                              
    >>> ...  article = self._extract_articles(url)
                              
    >>> ...  self._store_articles(article)
                          


+ Le script principal fait appel à la classe CollectArticle qui
  contient la définition des attributs et méthodes propres à
  l’extraction d’articles jusqu’au stockage.

::

    >>> from scraping_newspapers import CollectArticle
                              
    >>> ...  article = CollectArticle()
                              
    >>> ...  article.extract_from_source(source)
                          






Phase d’élaboration des évènements
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


+ Effectué via le script *clustering_articles.py*
+ Il traite “ **la classification automatique**”via *clustering*.
+ Pour ce faire, la librairie **sickitlearn** a été utilisé, en
  important le package **cluster**  L'approche par le Kmeans a été utilisée pour réaliser la
  classification.

::

    >>> from sklearn import cluster
                              
    >>> ...cluster.KMeans()


+ Chaque groupe obtenu après la classification est encore re-
  partitionner pour avoir des groupes d'articles beaucoup plus
  cohérents.
+ Durant chaque partitionnement, le nombre de cluster a été évalué à
  **5%** de l'effectif total.




Table des Matières
~~~~~~~~~~~~~~~~~~


+ `Introduction`_
+ `Premier aperçu d'Azot`_
+ Structure du projet
+ `Fonctionnement d’AZOT`_
+ `Contribuons au projet!`_




Related Topics
~~~~~~~~~~~~~~


+ `Documentation overview`_



2017, w3a. | Powered by `Sphinx 1.6.2`_ & `Alabaster 0.7.10`_

.. _Alabaster 0.7.10: https://github.com/bitprophet/alabaster
.. _Documentation overview: index.html
.. _Premier aperçu d'Azot: genindex.html
.. _Sphinx 1.6.2: http://sphinx-doc.org/
.. _ documentation: http://newspaper.readthedocs.io/en/latest/
.. _Fonctionnement d’AZOT: fonctionnement.html
.. _Contribuons au projet!: etat-projet.html
.. _newspaper: https://github.com/antsafi/newspaper.git


