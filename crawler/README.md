# Crawler Web 

## Description
Ce projet est un simple crawler web écrit en Python, conçu pour explorer et extraire des liens à partir d'un site web donné. Il prend en charge le crawling séquentiel ainsi que le crawling multi-thread pour une exécution plus rapide.

## Prérequis
- Python 3.x

## Installation
1. Clonez ce dépôt : `git clone https://github.com/Horeb136/indexation-web.git`
2. Accédez au répertoire du projet : `cd crawler`

## Fonctionnalités
1. **Exploration de liens** : Le crawler commence avec une URL de départ et explore les liens pour extraire de nouvelles URLs.

2. **Respect du fichier `robots.txt`** : Avant de crawler une page, le crawler vérifie les règles spécifiées dans le fichier `robots.txt` du site pour respecter les restrictions.

3. **Sitemap** : Le crawler prend en charge la découverte et le crawling des URLs à partir du fichier `sitemap.xml` d'un site.

4. **Stockage des URLs visitées** : Les URLs visitées sont stockées dans un fichier texte (`crawled_webpages.txt`), permettant de garder une trace des pages explorées.

5. **Base de données SQLite** : Les URLs et leur âge (temps écoulé depuis la visite) sont stockés dans une base de données SQLite (`crawler_db.sqlite`).

6. **Crawling Multi-thread** : Le crawler peut être exécuté en mode multi-thread pour accélérer le processus de crawling.

Structure du Projet
1. `crawler.py` : Contient la classe `Crawler` avec les fonctionnalités de crawling.

2. `main.py` : Fichier principal pour exécuter le crawler avec des arguments en ligne de commande.


## Utilisation
Pour exécuter le crawler, ouvrez un terminal et exécutez le fichier `main.py` avec les arguments nécessaires.

### Exemple d'utilisation (séquentiel) :

```bash
python main.py https://example.com --max_urls 50 --politeness_delay 5
```
### Exemple d'utilisation (multi-thread) :
```bash
python main.py https://example.com --max_urls 50 --politeness_delay 5 --multi_thread
```

## Contributeur
- [Horeb SEIDOU](https://github.com/Horeb136)

Merci de contribuer à ce projet ! 🚀