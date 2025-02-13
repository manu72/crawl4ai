"""
crawl4ai - A web crawler for AI applications
"""

from .core.crawler import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CrawlResult
from .strategies.markdown import DefaultMarkdownGenerator
from .crawlers.sequential import crawl_sequential
from .crawlers.sitemap import SitemapCrawler

__version__ = "0.1.0"

__all__ = [
    "AsyncWebCrawler",
    "BrowserConfig",
    "CrawlerRunConfig",
    "CrawlResult",
    "DefaultMarkdownGenerator",
    "crawl_sequential",
    "SitemapCrawler"
] 