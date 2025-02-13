import asyncio
import sys
from crawl4ai.crawlers.sitemap import SitemapCrawler
from crawl4ai.crawlers.sequential import crawl_sequential

# Constants for configuration
# BASE_URL = "https://docs.crawl4ai.com"
BASE_URL = "https://vaea.vic.gov.au"

async def main():
    try:
        sitemap_crawler = SitemapCrawler(BASE_URL)
        urls = sitemap_crawler.get_sitemap_urls()
        
        if urls:
            print(f"\nFound {len(urls)} unique URLs to crawl")
            await crawl_sequential(urls)
        else:
            print("\nNo URLs found to crawl")
            
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)