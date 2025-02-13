import asyncio
from pathlib import Path
from datetime import datetime
import sys
from crawl4ai import AsyncWebCrawler
from crawl4ai.utils.filename import generate_filename

# Constants for configuration
URLS_TO_CRAWL = [
    #"https://immi.homeaffairs.gov.au/what-we-do/whm-program/latest-news",
    "https://www.sbs.com.au/news/latest-news",
    "https://www.sbs.com.au/language/filipino/en"
    # Add more URLs as needed
]
OUTPUT_FILE_PREFIX = "sbs"  # Default prefix for files

async def main():
    try:
        # Create main output directory
        base_output_dir = Path("output")
        base_output_dir.mkdir(exist_ok=True)
        
        # Create subdirectory using OUTPUT_FILE_PREFIX
        output_dir = base_output_dir / OUTPUT_FILE_PREFIX
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