import time 
from urllib import robotparser
from urllib.parse import urljoin, unquote, urlparse
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import random
import ssl
import sqlite3
import threading
from queue import Queue

ssl._create_default_https_context = ssl._create_unverified_context

class Crawler : 
    def __init__(self, start_url, max_urls=50, politeness_delay=5, db_name="crawler/crawler_db.sqlite", num_threads=5) : 
        """
        Initialiseur de la classe Crawler.

        Paramètres :
        - start_url : URL de départ pour le crawling.
        - max_urls : Nombre maximum d'URLs à crawler.
        - politeness_delay : Délai de politesse en secondes entre les requêtes.
        - db_name : Nom de la base de données SQLite pour stocker les données.
        - num_threads : Nombre de threads pour le crawling multi-threaded.
        """
        self.start_url = start_url 
        self.max_urls = max_urls 
        self.politeness_delay = politeness_delay 
        self.visited_urls = set() 
        self.to_visit_urls = [start_url]
        self.crawled_urls = []
        self.last_page_download_time = 0
        # Initialiser la connexion à la base de données
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.timestamp = int(time.time())
        # Variables nécessaires pour le multi-threading
        self.num_threads = num_threads
        self.thread_queue = Queue()
        self.lock = threading.Lock()

    def is_valid_url(self, url) : 
        """
        Vérifie si une URL est valide.

        Paramètres :
        - url : URL à vérifier.

        Retourne :
        True si l'URL est valide, False sinon.
        """
        parsed_url = urlparse(url)
        return bool(parsed_url.netloc) and bool(parsed_url.scheme)
    
    def can_crawl(self, base_url) :
        """
        Vérifie si la page à l'URL donnée peut être crawlée en fonction du fichier robots.txt.

        Paramètres :
        - base_url : URL de la page à vérifier.

        Retourne :
        True si la page peut être crawlée, False sinon.
        """
        if not self.is_valid_url(base_url):
            return False
        else :  
            cleaned_url = unquote(base_url)
            parsed_url = urlparse(cleaned_url)
            rp = robotparser.RobotFileParser()
            rp.set_url(urljoin(parsed_url.scheme + "://" + parsed_url.netloc, "/robots.txt"))
            rp.read()
            return rp.can_fetch("*", base_url)
    
    def fetch_page(self, url) : 
        """
        Récupère le contenu HTML d'une page à partir de son URL.

        Paramètres :
        - url : URL de la page à récupérer.

        Retourne :
        Le contenu HTML de la page si la requête est réussie, None sinon.
        """
        try : 
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            if response.status_code == 200 : 
                self.last_page_download_time = end_time - start_time
                return response.text
            else : 
                return None
        except Exception as e :
            print(f"Error fetching page : {e}")
            return None
    
    def fetch_sitemap(self, sitemap_url) : 
        """
        Récupère la liste des URLs à partir d'un fichier sitemap XML.

        Paramètres :
        - sitemap_url : URL du fichier sitemap XML.

        Retourne :
        Liste des URLs du sitemap.
        """
        try :
            response = requests.get(sitemap_url)
            if response.status_code == 200 :
                tree = ET.fromstring(response.text)
                urls = [url.text for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
                return urls
            else : 
                print(f"Error fetching sitemap : {response.status_code}")
                return []
        except Exception as e :
            print(f"Error fetching sitemap : {e}")
            return []
    

    def extract_links(self, html_contents):
        """
        Extrait les liens (URLs) du contenu HTML de la page.

        Paramètres :
        - html_contents : Contenu HTML de la page.

        Cette fonction extrait les liens de la page et les ajoute à la liste des URLs à visiter.
        """
        random.seed(229)
        soup = BeautifulSoup(html_contents, 'html.parser')
        links = soup.find_all('a', href=True)
        links = random.sample(links, 5, ) if len(links) > 5 else links
        for link in links : 
            absolute_url = urljoin(self.start_url, link['href'])
            if absolute_url not in self.visited_urls and absolute_url not in self.to_visit_urls :
                self.to_visit_urls.append(absolute_url)

    def create_table(self):
        """
        Crée la table crawled_webpages dans la base de données SQLite si elle n'existe pas.
        """
        with self.conn:
            self.conn.execute('''
                                CREATE TABLE IF NOT EXISTS crawled_webpages 
                                (id INTEGER PRIMARY KEY, 
                                url TEXT, 
                                timestamp INTEGER, 
                                age INTEGER) ''')
            
    def insert_webpage(self, url, age):
        """
        Insère une page crawlée dans la base de données SQLite.

        Paramètres :
        - url : URL de la page crawlée.
        - age : Âge de la page en secondes.
        """
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO crawled_webpages (url,  age) VALUES (?, ?)', (url,  age))
    
    def write_to_file(self) :
        """
        Écrit les URLs visitées dans un fichier texte.
        """
        with open("./crawler/crawled_webpages.txt", "w") as f :
            for url in self.visited_urls : 
                f.write(url + "\n")
                print(f"Writing {url} in crawled_webpages.txt")

    def crawl(self):
        """
        Fonction principale pour le crawling séquentiel.
        """
        while self.to_visit_urls and len(self.visited_urls) < self.max_urls : 
            current_url = self.to_visit_urls.pop(0)
            if current_url.endswith("sitemap.xml"):
                self.to_visit_urls.extend(self.fetch_sitemap(current_url))
            else : 
                sitemap = current_url + "/sitemap.xml"
                self.to_visit_urls.extend(self.fetch_sitemap(sitemap))
                if not self.can_crawl(current_url) :
                    print(f"Skipping crawling {current_url} as it is not allowed by robots.txt")
                else : 
                    if current_url not in self.visited_urls :
                        print(f"Crawling {current_url}...")
                        html_contents = self.fetch_page(current_url)
                        if html_contents :
                            self.extract_links(html_contents)
                            self.visited_urls.add(current_url)
                            print(f"Visited URLs : {len(self.visited_urls)}")
                            print(f"To visit URLs : {len(self.to_visit_urls)}")

                            # Adjust politeness delay based on the last page download time
                            adjusted_delay = max(self.politeness_delay, self.last_page_download_time * 2)
                            time.sleep(adjusted_delay)

                            age = int(time.time()) - self.timestamp
                            self.insert_webpage(current_url, age)
                            self.timestamp = int(time.time())
        self.write_to_file()

    def insert_webpage_multi_thread(self, url, age):
        """
        Insère une page crawlée dans la base de données SQLite (version multi-thread).

        Paramètres :
        - url : URL de la page crawlée.
        - age : Âge de la page en secondes.
        """
        thread_id = threading.get_ident()
        connection = sqlite3.connect("crawler/crawler_db.sqlite")

        with connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO crawled_webpages (url, age) VALUES (?, ?)', (url, age))

    def process_page(self) : 
        """
        Fonction pour le traitement de chaque page dans le mode multi-threaded.
        """
        while True :
            current_url = self.thread_queue.get()
            if current_url is None :
                break

            if current_url.endswith("sitemap.xml"):
                self.to_visit_urls.extend(self.fetch_sitemap(current_url))
            else : 
                sitemap = current_url + "/sitemap.xml"
                self.to_visit_urls.extend(self.fetch_sitemap(sitemap))
                if not self.can_crawl(current_url) :
                    print(f"Skipping crawling {current_url} as it is not allowed by robots.txt")
                else : 
                    if current_url not in self.visited_urls :
                         with self.lock:
                            if len(self.visited_urls) < self.max_urls:
                                print(f"Crawling {current_url}...")
                                html_contents = self.fetch_page(current_url)
                                if html_contents :
                                    self.extract_links(html_contents)
                                    self.visited_urls.add(current_url)
                                    print(f"Visited URLs : {len(self.visited_urls)}")
                                    print(f"To visit URLs : {len(self.to_visit_urls)}")

                                    # Adjust politeness delay based on the last page download time
                                    adjusted_delay = max(self.politeness_delay, self.last_page_download_time * 2)
                                    time.sleep(adjusted_delay)

                                    age = int(time.time()) - self.timestamp
                                    self.insert_webpage_multi_thread(current_url, age)
            self.thread_queue.task_done()
    
    def multi_thread_crawl(self) :
        """
        Fonction principale pour le crawling en mode multi-threaded.
        """
        for i in range(self.num_threads) :
            thread = threading.Thread(target=self.process_page)
            thread.daemon = True
            thread.start()

            while self.to_visit_urls and len(self.visited_urls) < self.max_urls:
                current_url = self.to_visit_urls.pop(0)
                self.thread_queue.put(current_url)

            self.thread_queue.join()
            self.write_to_file()
