import time 
import argparse
from urllib import robotparser
import requests
from bs4 import BeautifulSoup

class SimpleCrawler : 
    def __init__(self, start_url, max_urls = 50, politeness_delay = 5) : 
        self.start_url = start_url 
        self.max_urls = max_urls 
        self.politeness_delay = politeness_delay 
        self.visited_urls = set() 
        self.robot_parser = self.setup_robot_parser(start_url)

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
    
    def crawl(self) : 
        queue = [self.start_url]

        while queue and len(self.visited_urls) < self.max_urls :
            current_url = queue.pop(0)

            if not self.can_crawl(current_url):
                print(f"Skipping crawling of {current_url} as it violates robots.txt rules")
            else :
                if current_url not in self.visited_urls : 
                    print(f"Visiting {current_url}")
                    self.visited_urls.add(current_url)
                    print(f"Visited {len(self.visited_urls)} URLs")

                    html_contents = self.fetch_page(current_url)

                    if html_contents : 
                        links = self.extract_links(html_contents)
                        queue.extend(links[ : 5])
                        print(f"Queue : {queue}")
                        time.sleep(self.politeness_delay)
        self.write_to_file()
    
    def write_to_file(self) :
        with open("./crawler/crawled_webpages.txt", "w") as f :
            for url in self.visited_urls : 
                f.write(url + "\n")
                print(f"Writing {url} in crawled_webpages.txt")
    
def main() : 
    parser = argparse.ArgumentParser(description="Simple Crawler")
    parser.add_argument("start_url", help="The starting URL to crawl")
    parser.add_argument("--max_urls", type=int, default=50, help="The maximum number of URLs to crawl")
    parser.add_argument("--politeness_delay", type=int, default=5, help="The politeness delay in seconds")
    args = parser.parse_args()

    crawler = SimpleCrawler(args.start_url, args.max_urls, args.politeness_delay)
    crawler.crawl()

if __name__ == "__main__" :
    main()