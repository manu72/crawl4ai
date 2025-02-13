import asyncio
from crawl4ai import AsyncWebCrawler
from pathlib import Path
from datetime import datetime
from crawl4ai.utils.filename import generate_filename
import sys

# Constants for configuration
URLS_TO_CRAWL = [
    "https://immi.homeaffairs.gov.au/what-we-do/whm-program/latest-news",
    "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing",
    # Add more URLs as needed
]
OUTPUT_FILE_PREFIX = "immi"  # Default prefix for files

async def main():
    try:
        # Create output directory if it doesn't exist
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate timestamp for this batch
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        async with AsyncWebCrawler() as crawler:
            for index, url in enumerate(URLS_TO_CRAWL, start=1):
                try:
                    print(f"\nProcessing {index}/{len(URLS_TO_CRAWL)}: {url}")
                    result = await crawler.arun(url=url)
                    
                    if result.markdown:
                        # Clean up the markdown before saving
                        cleaned_markdown = result.clean_markdown()
                        
                        # Generate filename using the same convention as crawl-sequential.py
                        filename = generate_filename(url, index, timestamp, OUTPUT_FILE_PREFIX)
                        output_file = output_dir / filename
                        
                        # Write the cleaned markdown content to file
                        output_file.write_text(cleaned_markdown)
                        print(f"✓ Successfully saved to: {output_file}")
                    else:
                        print("✗ Failed: No content retrieved")
                        
                except Exception as e:
                    print(f"✗ Error crawling {url}: {str(e)}")
                    
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)