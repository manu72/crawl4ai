# Custom web crawler and AI Agent

An intelligent web crawler designed to extract and process web content for AI applications. Built with Python, it supports async operations, configurable crawling strategies, and flexible content processing.

## Features

- 🚀 Asynchronous web crawling with session reuse
- 📑 Intelligent content extraction and markdown conversion
- 🗺️ Sitemap-based URL discovery
- 🔄 Configurable retry mechanisms and rate limiting
- 🎯 Multiple crawling strategies (sequential, parallel)
- 🎨 Customizable content processing
- 📁 Organized file output with meaningful names

## Installation

1. Clone the repository:
   bash
   git clone /yourusername/crawl4ai.git
   cd crawl4ai

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Basic Crawling

```python
from crawl4ai import AsyncWebCrawler

async with AsyncWebCrawler() as crawler:
    result = await crawler.arun("https://example.com")
    print(result.markdown)
```

### Sitemap Crawling

```python
from crawl4ai import SitemapCrawler
from crawl4ai.crawlers import crawl_sequential

sitemap_crawler = SitemapCrawler("https://example.com")
urls = sitemap_crawler.get_sitemap_urls()
await crawl_sequential(urls)
```

### Command Line Usage

```bash
# Crawl a website using its sitemap
python crawl-sequential.py

# Crawl specific pages in an array
python crawl-page.py

# Process and summarize crawled content
python agent.py output/
```

## Configuration

The crawler can be configured through environment variables or directly in code:

- `OPENAI_API_KEY`: Your OpenAI API key for content processing
- `MAX_PAGES_TO_SAVE`: Maximum number of pages to save (None for unlimited)
- `OUTPUT_FILE_PREFIX`: Prefix for output files
- `USER_AGENT`: Browser user agent string
- `TIMEOUT`: Request timeout in seconds
- `VERIFY_SSL`: Whether to verify SSL certificates
- `MAX_RETRIES`: Maximum number of retry attempts
- `DELAY_BETWEEN_REQUESTS`: Delay between requests in seconds
- `FOLLOW_LINKS`: Whether to follow links on crawled pages

## Project Structure

crawl4ai/
├── core/ # Core crawler functionality
├── strategies/ # Content processing strategies
├── utils/ # Utility functions
└── crawlers/ # Crawler implementations

## **AI Agent for Website Content Summarisation**

This AI Agent extends an existing website crawler by leveraging OpenAI's GPT-4 Turbo model to summarize website content retrieved from given URLs. The agent reads markdown files containing the website content, processes each file through the OpenAI API, and generates both individual page summaries and an overall website summary.

This tool helps in analyzing and condensing large amounts of web data, making it useful for research, content analysis, and documentation purposes.

### **Features**

- **Automated Summarization**: Generates concise summaries for each webpage.
- **Overall Website Summary**: Aggregates page summaries to create a structured overview of the website.
- **Secure API Handling**: Uses environment variables to store the OpenAI API key securely.
- **Extensible & Modular**: Easily integrates into existing web crawling pipelines.
- **Error Handling & Logging**: Provides meaningful error messages and logs for debugging.
- **Command-line Interface (CLI)**: Simple CLI interface for ease of use.

### **Installation**

**Prerequisites**
Ensure you have the following installed:

- Python **3.8+**
- `pip` (Python package manager)
- OpenAI Python SDK

**Setup Instructions**

1. **Clone the Repository (if applicable)**

   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [aiohttp](https://docs.aiohttp.org/) for async operations
- Uses [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML processing
- Integrates with [OpenAI](https://openai.com/) for content analysis
