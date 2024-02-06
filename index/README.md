# Indexeur de Contenu Web

Ce projet implémente un indexeur de contenu web en Python, divisé en plusieurs modules pour construire des index non positionnels, un index avec stemmer et un index positionnel à partir des données de pages web extraites.

## Structure du Projet

Le projet est organisé en deux modules principaux :

1. **`index.py` :** Ce module contient la classe `WebIndexer`, responsable de la construction des différents types d'index.

2. **`main.py` :** Ce module est utilisé pour l'exécution principale du programme, où l'indexeur est initialisé et appelé pour construire l'index.

## Modules et Fonctions Principales

### 1. `WebIndexer` (index.py)

- **`build_non_pos_index_title` :** Construit un index non positionnel pour les titres des pages web.
- **`build_non_pos_index_h1` :** Construit un index non positionnel pour les balises h1 des pages web.
- **`build_non_pos_index_content` :** Construit un index non positionnel pour le contenu des pages web.
- **`build_stemmed_non_pos_index_title` :** Construit un index non positionnel pour les titres des pages web en appliquant un stemmer.
- **`build_positional_index_title` :** Construit un index positionnel pour les titres des pages web.

### 2. `main` (main.py)

- **Initialisation :** Chargement des données des pages web à partir du fichier `crawled_urls.json`.
- **Création de l'Index :** Appel à la fonction spécifique de l'indexeur pour construire un type d'index.

## Exécution

1. Assurez-vous que Python est installé sur votre machine ainsi la librairie `nltk` que vous pouvez installer comme suit : 
```bash
pip install nltk
```
2. Exécutez le script principal `main.py` pour construire l'index souhaité.
   
```bash
python main.py
```

## Rendus 
1. **Fichiers d'Index** : Les fichiers JSON d'index sont sauvegardés dans le répertoire de travail.
 -  Index non positionnel pour les titres : `title.non_pos_index.json`
 -  Index non positionnel pour les balises h1 : `h1.non_pos_index.json`
 -  Index non positionnel pour le contenu : `content.non_pos_index.json`
 -  Index non positionnel avec stemming pour les titres : `mon_stemmer.title.non_pos_index.json`
 -  Index positionnel pour les titres : `title.pos_index.json`
2. **Fichiers de Métadonnées** : Un fichier `metadata.json` est généré avec des statistiques globales et des statistiques spécifiques à chaque document: 
### Statistiques Globales

-    **Nombre de Documents :** Le nombre total de documents web analysés.
-   **Nombre Total de Tokens :** Le nombre total de tokens dans tous les documents.
-    **Moyenne de Tokens par Document :** La moyenne du nombre de tokens par document.

### Statistiques Spécifiques à Chaque Document

Le fichier inclut également des statistiques spécifiques pour chaque document, enregistrées dans la liste `document_statistics`. Pour chaque document, les statistiques sont les suivantes :

-    **ID du Document :** L'identifiant unique du document.
-    **Nombre de Tokens dans le Titre :** Le nombre de tokens présents dans le titre.
-    **Nombre de Tokens dans les Balises h1 :** Le nombre de tokens présents dans les balises h1.
-    **Nombre de Tokens dans le Contenu :** Le nombre de tokens présents dans le contenu.

Ces statistiques sont utiles pour évaluer la distribution du contenu dans l'ensemble des documents web et pour obtenir des informations détaillées sur chaque document individuel.

3. **Journal d'Exécution** : L'exécution du programme affiche des messages de journalisation indiquant le progrès et les statistiques.


## Contributeur
- [Horeb SEIDOU](https://github.com/Horeb136)

Merci de contribuer à ce projet ! 🚀
