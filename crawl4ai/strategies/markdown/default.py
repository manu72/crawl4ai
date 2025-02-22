from bs4 import BeautifulSoup
from pydantic import BaseModel
from typing import Optional

class MarkdownGenerationStrategy(BaseModel):
    """Base class for markdown generation strategies"""
    title: Optional[str] = None
    
    def generate_markdown(self, html: str) -> str:
        raise NotImplementedError

class DefaultMarkdownGenerator(MarkdownGenerationStrategy):
    """Default strategy for converting HTML to markdown"""
    def generate_markdown(self, html: str) -> str:
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract title with error handling
            try:
                title_tag = soup.find('title')
                if title_tag:
                    self.title = title_tag.get_text().strip()
                    if len(self.title) == 0:
                        self.title = None
                else:
                    self.title = None
            except Exception as e:
                print(f"Warning: Could not extract title: {str(e)}")
                self.title = None
            
            # Remove script and style elements
            for element in soup(['script', 'style']):
                element.decompose()
                
            # Get text and clean up whitespace
            text = soup.get_text()
            
            # Clean up the text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error in markdown generation: {str(e)}")
            return "" 