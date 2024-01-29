import argparse
from crawler import Crawler

def main() : 
    parser = argparse.ArgumentParser(description="Simple Crawler")
    parser.add_argument("start_url", help="The starting URL to crawl")
    parser.add_argument("--max_urls", type=int, default=50, help="The maximum number of URLs to crawl")
    parser.add_argument("--politeness_delay", type=int, default=5, help="The politeness delay in seconds")
    args = parser.parse_args()

    crawler = Crawler(args.start_url, args.max_urls, args.politeness_delay)
    crawler.crawl()

if __name__ == "__main__" :
    main()