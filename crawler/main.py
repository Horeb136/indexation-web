import argparse
from crawler import Crawler

def main() : 
    parser = argparse.ArgumentParser(description="Simple Crawler")
    parser.add_argument("start_url", help="The starting URL to crawl")
    parser.add_argument("--max_urls", type=int, default=50, help="The maximum number of URLs to crawl")
    parser.add_argument("--politeness_delay", type=int, default=5, help="The politeness delay in seconds")
    parser.add_argument("--multi_thread", type=bool, default=False, help="Enable multi-threading")
    args = parser.parse_args()

    crawler = Crawler(args.start_url, args.max_urls, args.politeness_delay)
    if args.multi_thread :
        print("Multi-threading enabled")
        crawler.multi_thread_crawl()
    else :
        crawler.crawl()
if __name__ == "__main__" :
    main()