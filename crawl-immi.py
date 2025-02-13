import asyncio
from crawl4ai import *
from pathlib import Path
from datetime import datetime

# Constants for configuration
URLS_TO_CRAWL = [
    "https://immi.homeaffairs.gov.au/what-we-do/whm-program/latest-news",
    "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing",
    "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/work-holiday-417",
    "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/work-holiday-462",
    # Add more URLs as needed
]
OUTPUT_FILE_PREFIX = "immi"

async def main():
    # Create output directory if it doesn't exist
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Generate timestamp for this batch
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    async with AsyncWebCrawler() as crawler:
        for index, url in enumerate(URLS_TO_CRAWL, start=1):
            try:
                # Create numbered filename using index
                output_file = output_dir / f"{OUTPUT_FILE_PREFIX}_{index}_{timestamp}.md"
                
                result = await crawler.arun(url=url)
                
                # Clean up the markdown before saving
                cleaned_markdown = result.clean_markdown()
                
                # Write the cleaned markdown content to file
                output_file.write_text(cleaned_markdown)
                print(f"Content from {url} saved to: {output_file}")
                
            except Exception as e:
                print(f"Error crawling {url}: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())