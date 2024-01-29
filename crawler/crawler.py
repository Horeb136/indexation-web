import time 
from urllib import robotparser
from urllib.parse import urljoin, unquote, urlparse
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import random
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class Crawler : 
    def __init__(self, start_url, max_urls = 150, politeness_delay = 5) : 
        self.start_url = start_url 
        self.max_urls = max_urls 
        self.politeness_delay = politeness_delay 
        self.visited_urls = set() 
        self.to_visit_urls = [start_url]
        self.crawled_urls = []

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
            response = requests.get(url)
            if response.status_code == 200 : 
                return response.text
            else : 
                return None
        except Exception as e :
            print(f"Error fetching page : {e}")
            return None
        
    def extract_links(self, html_contents):
        random.seed(229)
        soup = BeautifulSoup(html_contents, 'html.parser')
        links = soup.find_all('a', href=True)
        links = random.sample(links, 5, ) if len(links) > 5 else links
        for link in links : 
            absolute_url = urljoin(self.start_url, link['href'])
            #print(f"Absolute link : {absolute_url}")
            if absolute_url not in self.visited_urls and absolute_url not in self.to_visit_urls :
                self.to_visit_urls.append(absolute_url)
   
    def write_to_file(self) :
        with open("./crawler/crawled_webpages.txt", "w") as f :
            for url in self.visited_urls : 
                f.write(url + "\n")
                print(f"Writing {url} in crawled_webpages.txt")

    def crawl(self) :
        #print(f"Sites to visites : \n {self.to_visit_urls}")
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
                        self.extract_links(html_contents)
                        print(f"Visited URLs : {len(self.visited_urls)}")

                        time.sleep(self.politeness_delay)
            #print(f"Sites to visites : \n {self.to_visit_urls}")
        self.write_to_file()
    