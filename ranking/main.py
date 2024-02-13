from webRanker import WebRanker

def main():
    ranker = WebRanker("./ranking/content_pos_index.json", "./ranking/documents.json")
    user_query = input("Entrez votre requête : ")
    results = ranker.rank_documents(user_query)
    ranker.display_results(results)

if __name__ == "__main__":
    main()