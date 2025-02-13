#!/usr/bin/env python3
import os
import openai
from pathlib import Path
import argparse
import logging

# Set up logging for debugging and error tracking.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Securely load the API key from an environment variable.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.error("OPENAI_API_KEY environment variable is not set.")
    exit(1)

# Initialize the OpenAI client
client = openai.OpenAI(api_key=api_key)

def call_chatgpt(prompt: str, model: str = "gpt-4-turbo", temperature: float = 0.7, max_tokens: int = 1024) -> str:
    """
    Calls the OpenAI API with the given prompt and returns the response.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
        )
        result = response.choices[0].message.content.strip()
        logger.debug("API call successful.")
        return result
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        raise

def summarize_text(text: str, prompt_template: str) -> str:
    """
    Inserts the text into the prompt template and returns the summarization.
    """
    prompt = prompt_template.format(text=text)
    return call_chatgpt(prompt)

def summarize_page(page_content: str) -> str:
    """
    Summarizes a single page's markdown content.
    """
    prompt_template = (
        "You are an expert content summarizer. Summarize the following webpage content "
        "in a few concise paragraphs, highlighting the main points and structure.\n\n{text}\n"
    )
    return summarize_text(page_content, prompt_template)

def summarize_website(pages: dict) -> str:
    """
    Produces an overall website summary by combining the individual page contents.
    """
    # Option 1: Combine page summaries and then summarize
    combined_summaries = ""
    for file_name, content in pages.items():
        page_summary = summarize_page(content)
        combined_summaries += f"Summary for {file_name}:\n{page_summary}\n\n"
    
    website_prompt = (
        "You are an expert website analyst. Based on the following summaries of website pages, "
        "produce a concise overall summary of the website. Highlight its key themes, purpose, "
        "and structure.\n\n{combined_summaries}"
    )
    prompt = website_prompt.format(combined_summaries=combined_summaries)
    return call_chatgpt(prompt)

def read_markdown_files(folder: str) -> dict:
    """
    Reads all markdown (*.md) files from the provided folder and returns a dictionary
    mapping file names to their content.
    """
    folder_path = Path(folder)
    if not folder_path.is_dir():
        raise ValueError(f"The path {folder} is not a valid directory.")
    
    pages = {}
    for md_file in folder_path.glob("*.md"):
        try:
            with md_file.open(encoding="utf-8") as f:
                pages[md_file.name] = f.read()
            logger.info(f"Loaded {md_file.name}")
        except Exception as e:
            logger.error(f"Error reading {md_file.name}: {e}")
    return pages

def main():
    parser = argparse.ArgumentParser(
        description="Summarize website content using the OpenAI ChatGPT API."
    )
    parser.add_argument("folder", help="Folder containing markdown files of website pages.")
    args = parser.parse_args()

    try:
        pages = read_markdown_files(args.folder)
    except Exception as e:
        logger.error(f"Failed to read markdown files: {e}")
        exit(1)
    
    if not pages:
        logger.error("No markdown files found in the specified folder.")
        exit(1)

    logger.info("Summarizing individual pages...")
    page_summaries = {}
    for file_name, content in pages.items():
        logger.info(f"Processing {file_name}...")
        try:
            summary = summarize_page(content)
            page_summaries[file_name] = summary
            print(f"\nSummary for {file_name}:\n{summary}\n{'-'*60}")
        except Exception as e:
            logger.error(f"Error summarizing {file_name}: {e}")

    logger.info("Summarizing overall website...")
    try:
        overall_summary = summarize_website(pages)
        print(f"\nOverall Website Summary:\n{overall_summary}\n{'='*60}")
    except Exception as e:
        logger.error(f"Error summarizing website: {e}")

if __name__ == "__main__":
    main()