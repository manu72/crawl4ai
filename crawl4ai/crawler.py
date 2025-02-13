import aiohttp
from bs4 import BeautifulSoup
from pydantic import BaseModel
import re
from .markdown_generation_strategy import DefaultMarkdownGenerator

class BrowserConfig(BaseModel):
    """Configuration for browser behavior"""
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    timeout: int = 30
    verify_ssl: bool = True

class CrawlerRunConfig(BaseModel):
    """Configuration for crawler run"""
    max_retries: int = 3
    delay_between_requests: float = 1.0
    follow_links: bool = False

class CrawlResult(BaseModel):
    markdown: str
    html: str = ""
    
    def clean_markdown(self):
        """Clean up the markdown content by removing excessive whitespace"""
        # Replace multiple blank lines with a single blank line
        cleaned = re.sub(r'\n\s*\n', '\n\n', self.markdown)
        # Remove leading/trailing whitespace from each line
        cleaned = '\n'.join(line.strip() for line in cleaned.splitlines())
        # Remove any leading/trailing blank lines
        cleaned = cleaned.strip()
        return cleaned

class AsyncWebCrawler:
    def __init__(self, 
                 browser_config: BrowserConfig = None, 
                 run_config: CrawlerRunConfig = None,
                 markdown_generator = None):
        self.session = None
        self.browser_config = browser_config or BrowserConfig()
        self.run_config = run_config or CrawlerRunConfig()
        self.markdown_generator = markdown_generator or DefaultMarkdownGenerator()
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(
            headers={"User-Agent": self.browser_config.user_agent},
            timeout=aiohttp.ClientTimeout(total=self.browser_config.timeout)
        )
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def arun(self, url: str) -> CrawlResult:
        async with self.session.get(url, ssl=self.browser_config.verify_ssl) as response:
            html = await response.text()
            markdown = self.markdown_generator.generate_markdown(html)
            result = CrawlResult(markdown=markdown, html=html)
            return result 