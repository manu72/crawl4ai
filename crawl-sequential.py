import asyncio
import sys
from crawl4ai.crawlers.sitemap import SitemapCrawler
from crawl4ai.crawlers.sequential import crawl_sequential

# Constants for configuration
# BASE_URL = "https://docs.crawl4ai.com"
# BASE_URL = "https://www.rba.gov.au"
BASE_URL = "https://vaea.vic.gov.au"
# BASE_URL = "https://www.coindesk.com"
# BASE_URL = "https://www.sbs.com.au/language/filipino/en"

# Sitemap Configuration
CUSTOM_SITEMAP_URL = "https://vaea.vic.gov.au/sitemap.xml"
MAIN_SITEMAP_URL = "https://vaea.vic.gov.au/sitemap.xml"
USE_CUSTOM_SITEMAP_ONLY = False  # Set to True to only use custom sitemap

# Output Configuration
# defined in sequential.py

async def main():
    try:
        urls = set()  # Use set to avoid duplicates
        
        # Get URLs from custom sitemap if provided
        if CUSTOM_SITEMAP_URL:
            sitemap_crawler = SitemapCrawler(BASE_URL)
            sitemap_crawler.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xml,application/xhtml+xml',
                'Accept-Language': 'en-US,en;q=0.9',
            })
            custom_urls = sitemap_crawler.get_urls_from_sitemap(CUSTOM_SITEMAP_URL)
            if custom_urls:
                print(f"\nFound {len(custom_urls)} URLs in custom sitemap")
                urls.update(custom_urls)
        
        # Get URLs from main sitemap if enabled
        if not USE_CUSTOM_SITEMAP_ONLY:
            sitemap_crawler = SitemapCrawler(BASE_URL, paths=[MAIN_SITEMAP_URL])
            standard_urls = sitemap_crawler.get_sitemap_urls()
            if standard_urls:
                # Filter URLs to only include those from the Filipino section
                filipino_urls = {url for url in standard_urls if '/language/filipino/' in url}
                print(f"\nFound {len(filipino_urls)} Filipino URLs in standard sitemaps")
                urls.update(filipino_urls)
        
        # Process combined URLs
        if urls:
            url_count = len(urls)
            print(f"\nTotal unique URLs to crawl: {url_count}")
            
            # Add confirmation prompt for large number of URLs
            if url_count > 100:
                confirmation = input(f"\nWarning: You are about to crawl {url_count} URLs. Do you want to continue? (y/n): ")
                if confirmation.lower() != 'y':
                    print("Operation cancelled by user")
                    return 0
            
            await crawl_sequential(list(urls))
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