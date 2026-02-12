import PyPDF2
from typing import List, Optional
import os

class PDFProcessor:
    """Handles PDF file processing and text extraction."""
    
    def __init__(self):
        self.current_pdf = None
        self.page_count = 0
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text as a string
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                self.page_count = len(pdf_reader.pages)
                
                for page_num, page in enumerate(pdf_reader.pages):
                    page_text = page.extract_text()
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            return text.strip()
        
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_page_text(self, pdf_path: str, page_number: int) -> str:
        """
        Extract text from a specific page.
        
        Args:
            pdf_path: Path to the PDF file
            page_number: Page number (0-indexed)
            
        Returns:
            Extracted text from the specified page
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if 0 <= page_number < len(pdf_reader.pages):
                    page = pdf_reader.pages[page_number]
                    return page.extract_text().strip()
                else:
                    return f"Error: Page {page_number + 1} does not exist"
        
        except Exception as e:
            print(f"Error extracting page text: {e}")
            return ""
    
    def extract_page_range(self, pdf_path: str, start_page: int, end_page: int) -> str:
        """
        Extract text from a range of pages.
        
        Args:
            pdf_path: Path to the PDF file
            start_page: Starting page number (0-indexed)
            end_page: Ending page number (0-indexed, inclusive)
            
        Returns:
            Extracted text from the specified page range
        """
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num in range(start_page, min(end_page + 1, len(pdf_reader.pages))):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    text += f"\n--- Page {page_num + 1} ---\n{page_text}\n"
            
            return text.strip()
        
        except Exception as e:
            print(f"Error extracting page range: {e}")
            return ""
    
    def get_page_count(self, pdf_path: str) -> int:
        """
        Get the total number of pages in a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Number of pages
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                return len(pdf_reader.pages)
        
        except Exception as e:
            print(f"Error getting page count: {e}")
            return 0
    
    def get_metadata(self, pdf_path: str) -> dict:
        """
        Extract metadata from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing PDF metadata
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = pdf_reader.metadata
                
                return {
                    'title': metadata.get('/Title', 'Unknown'),
                    'author': metadata.get('/Author', 'Unknown'),
                    'subject': metadata.get('/Subject', 'Unknown'),
                    'creator': metadata.get('/Creator', 'Unknown'),
                    'producer': metadata.get('/Producer', 'Unknown'),
                    'creation_date': metadata.get('/CreationDate', 'Unknown'),
                    'pages': len(pdf_reader.pages)
                }
        
        except Exception as e:
            print(f"Error extracting metadata: {e}")
            return {}
    
    def split_into_chunks(self, text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """
        Split text into overlapping chunks for processing.
        
        Args:
            text: Text to split
            chunk_size: Size of each chunk in characters
            overlap: Number of overlapping characters between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        
        return chunks
