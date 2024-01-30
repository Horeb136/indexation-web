# Crawler Web 

## Description
Ce projet est un simple crawler web écrit en Python, conçu pour explorer et extraire des liens à partir d'un site web donné. Il prend en charge le crawling séquentiel ainsi que le crawling multi-thread pour une exécution plus rapide.

## Contributeur
- [Horeb SEIDOU](https://github.com/Horeb136)

## Prérequis
- Python 3.x

## Installation
1. Clonez ce dépôt : `git clone https://github.com/Horeb136/indexation-web.git`
2. Accédez au répertoire du projet : `cd crawler`

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


