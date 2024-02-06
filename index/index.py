import json
import re
from collections import defaultdict
from nltk.stem import SnowballStemmer

class WebIndexer(): 
    def __init__(self) :
        self.index = defaultdict(list)
        self.document_stats = []

    def extract_tokens(self, text): 
        return re.findall(r'\b\w+\b', text.lower())
    
    # Definition du constructeur d'index de titres
    def build_non_pos_index_title(self, crawled_urls) : 
        num_documents = len(crawled_urls)
        self.index = defaultdict(list)

        for doc_id, doc, in enumerate(crawled_urls) :
            print(f"Indexing title of document of url {doc['url']}")    

            title_tokens = self.extract_tokens(doc['title'])

            doc_stats = {
                'document_id' : doc_id, 
                'title_tokens' : len(title_tokens),
            }
            print(f"Document title stats : {doc_stats}")
            self.document_stats.append(doc_stats)

            for token in title_tokens :
                if doc_id not in self.index[token] :
                    self.index[token].append(doc_id)
                
            print("\n")
            
        num_tokens = sum(len(token) for token in self.index.values())
        avg_tokens_per_doc = num_tokens / num_documents
        global_stats = {
            'num_documents' : num_documents,
            'total_title_tokens' : num_tokens,
            'avg_title_tokens_per_doc' : avg_tokens_per_doc
        }
        print(f"Global stats : {global_stats}")

        final_stats = {
            "global_title_statistics" : global_stats,
            "document_title_statistics" : self.document_stats,
        }

            # Sauvegarder l'index dans un fichier JSON
        with open("title.non_pos_index.json", "w") as index_file:
            json.dump(self.index, index_file, separators=(',', ':'), ensure_ascii=False)

        with open("metadata.json", "w") as metadata_file:
            json.dump(final_stats, metadata_file, indent=2)

        print("Indexing complete.")

    # Definition du constructeur d'index de h1 d'articles
    def build_non_pos_index_h1(self, crawled_urls) : 
        num_documents = len(crawled_urls)
        self.index = defaultdict(list)

        for doc_id, doc, in enumerate(crawled_urls) :
            print(f"Indexing h1 of document of url {doc['url']}")    

            h1_tokens = self.extract_tokens(doc['h1'])

            doc_stats = {
                'document_id' : doc_id, 
                'h1_tokens' : len(h1_tokens),
            }
            print(f"Document h1 stats : {doc_stats}")
            self.document_stats.append(doc_stats)

            for token in h1_tokens :
                if doc_id not in self.index[token] :
                    self.index[token].append(doc_id)
                
            print("\n")
            
        num_tokens = sum(len(token) for token in self.index.values())
        avg_tokens_per_doc = num_tokens / num_documents
        global_stats = {
            'num_documents' : num_documents,
            'total_h1_tokens' : num_tokens,
            'avg_h1_tokens_per_doc' : avg_tokens_per_doc
        }
        print(f"Global stats : {global_stats}")

        final_stats = {
            "global_h1_statistics" : global_stats,
            "document_h1_statistics" : self.document_stats,
        }

            # Save index to file
        with open("h1.non_pos_index.json", "w") as index_file:
            json.dump(self.index, index_file, indent=2)

        with open("metadata.json", "w") as metadata_file:
            json.dump(final_stats, metadata_file, separators=(',', ':'), ensure_ascii=False)

        print("Indexing complete.")

    # Definition du constructeur d'index de contenus d'articles
    def build_non_pos_index_content(self, crawled_urls) : 
        num_documents = len(crawled_urls)
        self.index = defaultdict(list)

        for doc_id, doc, in enumerate(crawled_urls) :
            print(f"Indexing content of document of url {doc['url']}")    

            content_tokens = self.extract_tokens(doc['content'])

            doc_stats = {
                'document_id' : doc_id, 
                'content_tokens' : len(content_tokens),
            }
            print(f"Document content stats : {doc_stats}")
            self.document_stats.append(doc_stats)

            for token in content_tokens :
                if doc_id not in self.index[token] :
                    self.index[token].append(doc_id)
                
            print("\n")
            
        num_tokens = sum(len(token) for token in self.index.values())
        avg_tokens_per_doc = num_tokens / num_documents
        global_stats = {
            'num_documents' : num_documents,
            'total_content_tokens' : num_tokens,
            'avg_content_tokens_per_doc' : avg_tokens_per_doc
        }
        print(f"Global stats : {global_stats}")

        final_stats = {
            "global_content_statistics" : global_stats,
            "document_content_statistics" : self.document_stats,
        }

            # Save index to file
        with open("content.non_pos_index.json", "w") as index_file:
            json.dump(self.index, index_file, separators=(',', ':'), ensure_ascii=False)

        with open("metadata.json", "w") as metadata_file:
            json.dump(final_stats, metadata_file, indent=2)

        print("Indexing complete.")

        #################### INDEX WITH STEMMER ####################
    def stem_tokens(self, tokens):
        stemmer = SnowballStemmer("french")
        return [stemmer.stem(token) for token in tokens]
        
    def build_stemmed_non_pos_index_title(self, crawled_urls) : 
        num_documents = len(crawled_urls)
        self.index = defaultdict(list)

        for doc_id, doc, in enumerate(crawled_urls) :
            print(f"Indexing title of document of url {doc['url']}")    

            title_tokens = self.extract_tokens(doc['title'])
            stemmed_title_tokens = self.stem_tokens(title_tokens)

            doc_stats = {
                'document_id' : doc_id, 
                'title_tokens' : len(stemmed_title_tokens),
            }
            print(f"Document title stats : {doc_stats}")
            self.document_stats.append(doc_stats)

            for token in stemmed_title_tokens :
                if doc_id not in self.index[token] :
                    self.index[token].append(doc_id)
                
            print("\n")
            
        num_tokens = sum(len(token) for token in self.index.values())
        avg_tokens_per_doc = num_tokens / num_documents
        global_stats = {
            'num_documents' : num_documents,
            'total_title_tokens' : num_tokens,
            'avg_title_tokens_per_doc' : avg_tokens_per_doc
        }
        print(f"Global stats : {global_stats}")

        final_stats = {
            "global_title_statistics" : global_stats,
            "document_title_statistics" : self.document_stats,
        }

        # Sauvegarder l'index avec stemming dans un fichier JSON
        with open("mon_stemmer.title.non_pos_index.json", "w") as index_file:
            json.dump(self.index, index_file, separators=(',', ':'), ensure_ascii=False)

        with open("metadata_stemmer.json", "w") as metadata_file:
            json.dump(final_stats, metadata_file, indent=2)

        print("Indexing complete with stemming.")
    
    ###################### INDEX POSITIONNEL ######################
    def build_positional_index_title(self, crawled_urls) : 
        num_documents = len(crawled_urls)
        self.index = defaultdict(list)

        for doc_id, doc, in enumerate(crawled_urls) :
            print(f"Indexing title of document of url {doc['url']}")    

            title_tokens = self.extract_tokens(doc['title'])
            stemmed_title_tokens = self.stem_tokens(title_tokens)

            doc_stats = {
                'document_id' : doc_id, 
                'title_tokens' : len(stemmed_title_tokens),
            }
            print(f"Document title stats : {doc_stats}")
            self.document_stats.append(doc_stats)

            for position, token in enumerate(stemmed_title_tokens):
                self.index[token].append([doc_id, position])
                
            print("\n")
            
        num_tokens = sum(len(postings) for postings in self.index.values())
        avg_tokens_per_doc = num_tokens / num_documents
        global_stats = {
            'num_documents' : num_documents,
            'total_title_tokens' : num_tokens,
            'avg_title_tokens_per_doc' : avg_tokens_per_doc
        }
        print(f"Global stats : {global_stats}")

        final_stats = {
            "global_title_statistics" : global_stats,
            "document_title_statistics" : self.document_stats,
        }

        # Sauvegarder l'index positionnel dans un fichier JSON
        with open("title.pos_index.json", "w") as index_file:
            json.dump(self.index, index_file, separators=(',', ':'), ensure_ascii=False)

        with open("metadata_pos.json", "w") as metadata_file:
            json.dump(final_stats, metadata_file, indent=2)

        print("Positional indexing complete.")