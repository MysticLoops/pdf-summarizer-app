"""
Utilities package for PDF Summarizer & Note-Taking Tool.

This package contains helper modules for:
- PDF processing and text extraction
- AI-powered text summarization
- Note management and export
- Text-to-speech audio generation
- MongoDB database integration
"""

from .pdf_processor import PDFProcessor
from .summarizer import Summarizer
from .note_manager import NoteManager
from .audio_player import AudioPlayer
from .database import Database

__all__ = [
    'PDFProcessor',
    'Summarizer',
    'NoteManager',
    'AudioPlayer',
    'Database'
]
