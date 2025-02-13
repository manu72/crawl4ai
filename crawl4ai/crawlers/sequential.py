from pathlib import Path
from datetime import datetime
from typing import List
from ..core.crawler import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
from ..strategies.markdown import DefaultMarkdownGenerator
from ..utils.filename import generate_filename

# Constants can be moved to a config file or environment variables
SAVE_MARKDOWN = True
OUTPUT_FILE_PREFIX = "vaea"
MAX_PAGES_TO_SAVE = None # None for unlimited

async def crawl_sequential(urls: List[str]):
    print("\n=== Sequential Crawling with Session Reuse ===")
    
    # Track number of pages saved
    pages_saved = 0

    # Create output directory if markdown saving is enabled
    output_dir = None
    timestamp = None
    if SAVE_MARKDOWN:

         # Create main output directory
        base_output_dir = Path("output")
        base_output_dir.mkdir(exist_ok=True)
        
        # Create subdirectory using OUTPUT_FILE_PREFIX
        output_dir = base_output_dir / OUTPUT_FILE_PREFIX
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    browser_config = BrowserConfig(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        timeout=30,
        verify_ssl=True
    )

    crawl_config = CrawlerRunConfig(
        max_retries=3,
        delay_between_requests=1.0,
        follow_links=False
    )

    async with AsyncWebCrawler(
        browser_config=browser_config,
        run_config=crawl_config,
        markdown_generator=DefaultMarkdownGenerator()
    ) as crawler:
        total = len(urls)
        for index, url in enumerate(urls, 1):
            try:
                print(f"\nProcessing {index}/{total}: {url}")
                result = await crawler.arun(url=url)
                if result.markdown:
                    cleaned_markdown = result.clean_markdown()
                    print(f"✓ Successfully crawled ({len(cleaned_markdown)} chars)")
                    
                    # Save to markdown file if enabled and within limit
                    if (SAVE_MARKDOWN and output_dir and timestamp and 
                        (MAX_PAGES_TO_SAVE is None or pages_saved < MAX_PAGES_TO_SAVE)):
                        filename = generate_filename(url, index, timestamp, OUTPUT_FILE_PREFIX)
                        output_file = output_dir / filename
                        output_file.write_text(cleaned_markdown)
                        print(f"  Saved to: {output_file}")
                        pages_saved += 1
                        
                        if MAX_PAGES_TO_SAVE and pages_saved >= MAX_PAGES_TO_SAVE:
                            print(f"\nReached maximum number of pages to save ({MAX_PAGES_TO_SAVE})")
                else:
                    print("✗ Failed: No content retrieved")
            except Exception as e:
                print(f"✗ Error: {str(e)}") 