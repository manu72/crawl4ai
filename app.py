import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing",
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())