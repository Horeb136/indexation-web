import time 
from urllib import robotparser
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

class Crawler : 
    def __init__(self, start_url, max_urls = 50, politeness_delay = 5) : 
        self.start_url = start_url 
        self.max_urls = max_urls 
        self.politeness_delay = politeness_delay 
        self.visited_urls = set() 
        self.robot_parser = self.setup_robot_parser(start_url)
        self.to_visit_urls = [start_url]
        self.crawled_urls = []

    def setup_robot_parser(self, base_url) :
        rp = robotparser.RobotFileParser()
        rp.set_url(base_url + "/robots.txt")
        rp.read()
        return rp
    
    def can_crawl(self, url) : 
        return self.robot_parser.can_fetch("*", url)

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
        soup = BeautifulSoup(html_contents, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True)]
        print(f"Found {len(links)} links")
        return links
    
    def read_sitemap(self, url) : 
        sitemap_url = url + "/sitemap.xml"
        print(f"Reading sitemap from {sitemap_url}")
        try : 
            response = requests.get(sitemap_url)
            print(f"Response status code : {response.status_code}")
            if response.status_code == 200 : 
                root = ET.fromstring(response.text)
                urls = [loc.text for loc in root.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
                print(f"Found {len(urls)} URLs in sitemap")
                return urls
        except Exception as e :
            print(f"Error reading sitemap from {sitemap_url}: {e}")
            return []


    def write_to_file(self) :
        with open("./crawler/crawled_webpages.txt", "w") as f :
            for url in self.visited_urls : 
                f.write(url + "\n")
                print(f"Writing {url} in crawled_webpages.txt")

    def crawl(self) : 
        sitemap_urls = self.read_sitemap(self.start_url)
        print(f"Sitemap URLs : {sitemap_urls}")
        queue = sitemap_urls if sitemap_urls else [self.start_url]

        while queue and len(self.visited_urls) < self.max_urls :
            current_url = queue.pop(0)
            
            if not self.can_crawl(current_url) :
                print(f"Skipping crawling {current_url} as it is not allowed by robots.txt")

            else : 
                if current_url not in self.visited_urls :
                    self.visited_urls.add(current_url)
                    print(f"Crawling {current_url} ... ")
                    print(f"Visited URLs : {len(self.visited_urls)}")

                    html_contents = self.fetch_page(current_url)

                    if html_contents :
                        links = self.extract_links(html_contents)
                        queue.extend(links[ : 5])
                        print(f"Queue : {queue}")
                        time.sleep(self.politeness_delay)       
        
        self.write_to_file()
    


    
    