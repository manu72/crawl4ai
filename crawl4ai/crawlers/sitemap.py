import requests
from typing import List
from xml.etree import ElementTree
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

# Default sitemap paths to check
DEFAULT_SITEMAP_PATHS = [
    "/sitemap.xml",           # Standard sitemap
    "/sitemap_index.xml",     # Sitemap index
    "/sitemaps/sitemap.xml",  # Common alternate location
    "/wp-sitemap.xml",        # WordPress format
]

class SitemapCrawler:
    """Crawler for extracting URLs from XML sitemaps"""
    
    def __init__(self, base_url: str, paths: List[str] = None):
        self.base_url = base_url.rstrip('/')
        self.paths = paths or DEFAULT_SITEMAP_PATHS.copy()
        self.namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        self.session = requests.Session()
        self.found_urls = set()  # Use set to avoid duplicates

    def get_sitemap_urls(self) -> List[str]:
        """Try different sitemap paths and collect all URLs."""
        # First, try to get sitemaps from robots.txt
        self._add_robots_sitemaps()
        
        # Then try all known paths
        for path in self.paths:
            sitemap_url = urljoin(self.base_url, path)
            try:
                urls = self._process_sitemap(sitemap_url)
                if urls:
                    print(f"Successfully found sitemap at: {sitemap_url}")
                    return list(urls)  # Convert set to list
            except Exception as e:
                print(f"Failed to process sitemap at {sitemap_url}: {str(e)}")
        
        if not self.found_urls:
            print("No sitemaps found at any of the standard locations")
        return list(self.found_urls)

    def _add_robots_sitemaps(self) -> None:
        """Check robots.txt for Sitemap directives and add them to paths."""
        robots_url = urljoin(self.base_url, "/robots.txt")
        try:
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            sitemap_urls = rp.site_maps()
            
            if sitemap_urls:
                print(f"Found {len(sitemap_urls)} sitemaps in robots.txt")
                for sitemap in sitemap_urls:
                    # Convert absolute URLs to paths
                    if sitemap.startswith(self.base_url):
                        path = urlparse(sitemap).path
                    else:
                        path = sitemap
                    
                    if path not in self.paths:
                        self.paths.append(path)
                        print(f"Added sitemap from robots.txt: {path}")
            
        except Exception as e:
            print(f"Note: Could not process robots.txt ({str(e)})")

    def _process_sitemap(self, sitemap_url: str) -> set:
        """Process a sitemap or sitemap index file."""
        response = self.session.get(sitemap_url, timeout=30)
        response.raise_for_status()
        
        root = ElementTree.fromstring(response.content)
        
        # Check if this is a sitemap index
        if 'sitemapindex' in root.tag:
            return self._process_sitemap_index(root)
        
        # Regular sitemap
        return self._extract_urls_from_sitemap(root)

    def _process_sitemap_index(self, root: ElementTree.Element) -> set:
        """Process a sitemap index file containing multiple sitemaps."""
        urls = set()
        for sitemap in root.findall('.//ns:loc', self.namespace):
            try:
                sub_urls = self._process_sitemap(sitemap.text)
                urls.update(sub_urls)
            except Exception as e:
                print(f"Error processing sub-sitemap {sitemap.text}: {str(e)}")
        return urls

    def _extract_urls_from_sitemap(self, root: ElementTree.Element) -> set:
        """Extract URLs from a regular sitemap file."""
        return {
            loc.text for loc in root.findall('.//ns:loc', self.namespace)
            if self._is_valid_url(loc.text)
        }

    def _is_valid_url(self, url: str) -> bool:
        """Basic URL validation."""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False 