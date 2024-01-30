import time 
from urllib import robotparser
from urllib.parse import urljoin, unquote, urlparse
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import random
import ssl
import sqlite3
import concurrent.futures

ssl._create_default_https_context = ssl._create_unverified_context

class Crawler : 
    def __init__(self, start_url, max_urls = 50, politeness_delay = 5, db_name = "crawler/crawler_db.sqlite") : 
        self.start_url = start_url 
        self.max_urls = max_urls 
        self.politeness_delay = politeness_delay 
        self.visited_urls = set() 
        self.to_visit_urls = [start_url]
        self.crawled_urls = []
        self.last_page_download_time = 0
        #Initialiser la connexion à la base de données
        self.conn = sqlite3.connect(db_name)
        self.create_table()
        self.timestamp = 0

    def can_crawl(self, base_url) :
        if base_url.startswith("mailto:") :
            return False
        else :  
            cleaned_url = unquote(base_url)
            parsed_url = urlparse(cleaned_url)
            rp = robotparser.RobotFileParser()
            rp.set_url(urljoin(parsed_url.scheme + "://" + parsed_url.netloc, "/robots.txt"))
            rp.read()
            return rp.can_fetch("*", base_url)
    
    def fetch_page(self, url) : 
        try : 
            start_time = time.time()
            response = requests.get(url)
            end_time = time.time()
            if response.status_code == 200 : 
                self.last_page_dowload_time = end_time - start_time
                return response.text
            else : 
                return None
        except Exception as e :
            print(f"Error fetching page : {e}")
            return None
    
    def fetch_sitemap(self, base_url) : 
        sitemap_url = urljoin(base_url, "/sitemap.xml")
        try :
            response = requests.get(sitemap_url)
            if response.status_code == 200 :
                tree = ET.fromstring(response.text)
                urls = [url.text for url in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
                return urls
        except Exception as e :
            print(f"Error fetching sitemap : {e}")
            return []

    def extract_links(self, html_contents):
        random.seed(229)
        soup = BeautifulSoup(html_contents, 'html.parser')
        links = soup.find_all('a', href=True)
        links = random.sample(links, 10, ) if len(links) > 10 else links
        for link in links : 
            absolute_url = urljoin(self.start_url, link['href'])
            #print(f"Absolute link : {absolute_url}")
            if absolute_url not in self.visited_urls and absolute_url not in self.to_visit_urls :
                self.to_visit_urls.append(absolute_url)
   
    def create_table(self):
        with self.conn:
            self.conn.execute('''
                                CREATE TABLE IF NOT EXISTS crawled_webpages 
                                (id INTEGER PRIMARY KEY, 
                                url TEXT, 
                                timestamp INTEGER, 
                                age INTEGER) ''')
            
    def insert_webpage(self, url, age):
        timestamp = int(time.time())
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO crawled_webpages (url,  age) VALUES (?, ?)', (url,  age))
            self.timestamp = timestamp
    
    def write_to_file(self) :
        with open("./crawler/crawled_webpages.txt", "w") as f :
            for url in self.visited_urls : 
                f.write(url + "\n")
                print(f"Writing {url} in crawled_webpages.txt")

    def crawl(self) :
        #print(f"Sites to visit : \n {self.to_visit_urls}")
        while self.to_visit_urls and len(self.visited_urls) < self.max_urls :
            current_url = self.to_visit_urls.pop(0)

            if not self.can_crawl(current_url) :
                print(f"Skipping crawling {current_url} as it is not allowed by robots.txt")
                
            else : 
                if current_url not in self.visited_urls : 
                    print(f"Crawling {current_url} ... ")
                    html_contents = self.fetch_page(current_url)
                    if html_contents : 
                        self.extract_links(html_contents)
                        self.visited_urls.add(current_url)
                        print(f"Visited URLs : {len(self.visited_urls)}")
                        print(f"To visit URLs : {len(self.to_visit_urls)}")

                        # Fetch and add URLs from sitemap
                        sitemap_urls = self.fetch_sitemap(current_url)
                        for sitemap_url in sitemap_urls :
                            #print(f"Fetching sitemap for {sitemap_url} ... ")
                            if sitemap_url not in self.visited_urls and sitemap_url not in self.to_visit_urls :
                                self.to_visit_urls.append(sitemap_url)
                        print(f"To visit URLs after sitemap : {len(self.to_visit_urls)}")

                        # Adjust politeness delay based on the last page download time
                        adjusted_delay = max(self.politeness_delay, self.last_page_download_time * 2)
                        time.sleep(adjusted_delay)

                        age = int(time.time()) - self.timestamp
                        self.insert_webpage(current_url, age)
            #print(f"Sites to visites : \n {self.to_visit_urls}")
        self.write_to_file()
    
    ###########################################MULTI-THREAD CRAWL######################################
    def process_page(self, current_url) : 
        if not self.can_crawl(current_url) :
                print(f"Skipping crawling {current_url} as it is not allowed by robots.txt")
                return
        
        else : 
            if current_url not in self.visited_urls : 
                print(f"Crawling {current_url} ... ")
                html_contents = self.fetch_page(current_url)

                if html_contents : 
                    self.extract_links(html_contents)
                    self.visited_urls.add(current_url)
                    print(f"Visited URLs : {len(self.visited_urls)}")
                    print(f"To visit URLs : {len(self.to_visit_urls)}")

                    # Fetch and add URLs from sitemap
                    sitemap_urls = self.fetch_sitemap(current_url)
                    for sitemap_url in sitemap_urls :
                        #print(f"Fetching sitemap for {sitemap_url} ... ")
                        if sitemap_url not in self.visited_urls and sitemap_url not in self.to_visit_urls :
                            self.to_visit_urls.append(sitemap_url)
                    print(f"To visit URLs after sitemap : {len(self.to_visit_urls)}")

                    # Adjust politeness delay based on the last page download time
                    adjusted_delay = max(self.politeness_delay, self.last_page_download_time * 2)
                    time.sleep(adjusted_delay)

                    age = int(time.time()) - self.timestamp
                    self.insert_webpage(current_url, age)
    
    def multi_thread_crawl(self) :
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            while self.to_visit_urls and len(self.visited_urls) < self.max_urls :
                current_url = self.to_visit_urls.pop(0)
                executor.submit(self.process_page, current_url)
        self.write_to_file()
