import json
from collections import defaultdict
import re

class WebRanker:
    def __init__(self, index_filename, urls_document):
        self.index_filename = index_filename
        self.urls_document = urls_document
        self.index = self.load_index()
        self.documents = self.load_documents()

    def load_index(self):
        with open(self.index_filename, "r") as index_file:
            return json.load(index_file)

    def load_documents(self):
        with open(self.urls_document, 'r') as f:
            crawled_urls = json.load(f)
        return crawled_urls

    def process_query(self, user_query):
        return re.findall(r'\b\w+\b', user_query.lower())

    def linear_ranking(self, document_id, query_tokens):
        counts = list()
        for token in query_tokens:
            if token in self.index:
                token_keys = self.index[token].keys()
                if document_id in token_keys:
                    counts.append(self.index[token][document_id]["count"])
        return sum(counts)

    def rank_documents(self, user_query):
        # Traitement de la requête
        query_tokens = self.process_query(user_query)

        # Liste pour stocker les résultats avec leurs scores
        results = []

        # Pour chaque document, calculer le score
        for doc_id, _ in enumerate(self.documents):
            score = self.linear_ranking(str(doc_id), query_tokens)
            if score > 0:
                results.append({"document_id": doc_id, "score": score})
        # Trier les résultats par score décroissant
        results.sort(key=lambda x: x["score"], reverse=True)

        # Sauvegarder les résultats dans un fichier JSON
        with open("./ranking/results.json", "w") as f:
            json.dump(results, f)

        return results

    def display_results(self, results):
        # Afficher les résultats (étape 6)
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
