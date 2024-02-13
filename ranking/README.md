# README

## Projet de Ranking avec WebRanker

Ce projet propose une application de ranking de documents basée sur un index positionnel et des méthodes de ranking linéaire et BM25. Le code est organisé dans la classe `WebRanker`.

### Organisation du Code

- **webRanker.py** : Contient la classe `WebRanker` qui gère le ranking des documents.
  
- **main.py** : Script principal pour lancer le ranking en utilisant la classe `WebRanker`.

### Installation

Assurez-vous d'avoir les bibliothèques nécessaires installées en exécutant la commande suivante :

```bash
pip install nltk
```
### Utilisation
Utilisation
Pour lancer le ranking, exécutez le script `main.py` depuis la racine du projet. Entrez votre requête lorsque vous y êtes invité.
```bash
python main.py 
```

### Classe WebRanker

La classe `WebRanker` comporte les méthodes principales suivantes :

- **`linear_ranking(document_id, query_tokens)`** : Calcule le score de ranking linéaire pour un document donné.

- **`bm25_score(document_id, query_tokens)`** : Calcule le score BM25 pour un document donné.

- **`rank_documents(user_query, bm25=False)`** : Classe les documents en fonction de la requête de l'utilisateur. Si `bm25` est défini sur `True`, utilise le score BM25 ; sinon, utilise le ranking linéaire.

- **`display_results(results)`** : Affiche les résultats du ranking.

Ces méthodes sont utilisées pour traiter la requête de l'utilisateur et produire le classement des documents en fonction du score choisi (linéaire ou BM25). Le résultat peut être affiché avec la méthode `display_results`.


### Fonctions de Ranking

#### Ranking Linéaire

La méthode `linear_ranking` attribue un poids plus élevé aux termes non-stop words lors du calcul du score de ranking linéaire.

#### BM25

La méthode `bm25_score` est basée sur le modèle BM25. Elle prend en compte la fréquence du terme, l'inverse de la fréquence du document, et la longueur moyenne des documents pour calculer le score BM25.

Pour plus de détails, référez-vous au code source et aux commentaires dans le fichier `webRanker.py`.



## Contributeur
- [Horeb SEIDOU](https://github.com/Horeb136)

Merci de contribuer à ce projet ! 🚀
