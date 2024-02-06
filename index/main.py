from index import WebIndexer
import json

def main():
    # Charger crawled_urls depuis le fichier JSON
    with open('crawled_urls.json', 'r') as f:
        crawled_urls = json.load(f)

    # Initialiser l'indexeur
    indexer = WebIndexer()
    
    # Construire l'index et obtenir les statistiques globales
    indexer.build_positional_index_title(crawled_urls)

if __name__ == "__main__":
    main()