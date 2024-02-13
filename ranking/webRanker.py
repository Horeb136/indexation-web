import json
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
import math

class WebRanker:
    def __init__(self, index_filename, urls_document, k=1.5, b=0.75):
        # Initialisation de l'objet WebRanker avec le fichier d'index, le fichier des URLs des documents,
        # et des paramètres optionnels pour le modèle BM25.
        self.index_filename = index_filename
        self.urls_document = urls_document
        self.index = self.load_index()
        self.documents = self.load_documents()
        self.stop_words = set(stopwords.words("french"))
        self.k = k
        self.b = b

    def load_index(self):
        # Fonction pour charger l'index depuis le fichier JSON.
        with open(self.index_filename, "r") as index_file:
            return json.load(index_file)

    def load_documents(self):
        # Fonction pour charger les documents depuis le fichier JSON contenant les URLs.
        with open(self.urls_document, 'r') as f:
            crawled_urls = json.load(f)
        return crawled_urls

    def process_query(self, user_query):
        # Fonction pour traiter la requête de l'utilisateur en la tokenisant.
        return re.findall(r'\b\w+\b', user_query.lower())
    
    def linear_ranking(self, document_id, query_tokens):
        # Fonction pour calculer le score de ranking linéaire d'un document pour une requête.
        counts = list()
        for token in query_tokens:
            if token in self.index:
                token_keys = self.index[token].keys()
                if document_id in token_keys:
                    # Appliquer une pondération en fonction du statut de stop word
                    weight = 2.0 if token not in self.stop_words else 1.0
                    counts.append(self.index[token][document_id]["count"] * weight)
        return sum(counts)
    
    def bm25_score(self, document_id, query_tokens):
        # Fonction pour calculer le score BM25 d'un document pour une requête.
        score = 0
        doc_length = sum(self.index[token][document_id]["count"] for token in self.index if document_id in self.index[token])
        for token in query_tokens:
            if token in self.index and document_id in self.index[token]:
                term_freq = self.index[token][document_id]["count"]
                idf = math.log((len(self.documents) - len(self.index[token]) + 0.5) / (len(self.index[token]) + 0.5) + 1.0)
                numerator = term_freq * (self.k + 1)
                denominator = term_freq + self.k * (1 - self.b + self.b * doc_length / self.average_doc_length())
                score += idf * numerator / denominator
        return score
    
    def average_doc_length(self):
        # Fonction pour calculer la longueur moyenne des documents dans l'index.
        total_length = 0
        total_docs = 0

        for doc_id in range(len(self.documents)):
            for token in self.index:
                if doc_id in self.index[token]:
                    total_length += self.index[token][doc_id]["count"]
            total_docs += 1

        # Éviter une division par zéro
        if total_docs != 0:
            return total_length / total_docs
        else:
            return 0

    def rank_documents(self, user_query, bm25=False):
        # Fonction principale pour classer les documents en fonction de la requête.
        # Traitement de la requête
        query_tokens = self.process_query(user_query)

        # Liste pour stocker les résultats avec leurs scores
        results = []

        # Pour chaque document, calculer le score
        for doc_id, _ in enumerate(self.documents):
            score = self.bm25_score(str(doc_id), query_tokens) if bm25 else self.linear_ranking(str(doc_id), query_tokens) 
            if score > 0:
                results.append({"document_id": doc_id, "score": score})
        # Trier les résultats par score décroissant
        results.sort(key=lambda x: x["score"], reverse=True)

        # Sauvegarder les résultats dans un fichier JSON
        with open("./ranking/results.json", "w") as f:
            json.dump(results, f)

        return results

    def display_results(self, results):
        # Fonction pour afficher les résultats.
        print("Résultats de la requête :")
        for result in results:
            doc_id = result["document_id"]
            doc_title = self.documents[doc_id]["title"]
            doc_url = self.documents[doc_id]["url"]
            print(f"Score: {result['score']} - Titre: {doc_title} - URL: {doc_url}")

# Exemple d'utilisation de la classe WebRanker
if __name__ == "__main__":
    ranker = WebRanker("./ranking/content_pos_index.json", "./ranking/documents.json")
    user_query = "Les jeux olympiques"
    results = ranker.rank_documents(user_query)
    ranker.display_results(results)
