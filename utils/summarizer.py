from typing import List, Optional
import os
import re

class Summarizer:
    """Handles text summarization using various AI models and techniques."""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY', '')
        self.model_available = bool(self.api_key)
    
    def summarize(self, text: str, length: str = "Moderate") -> str:
        """
        Generate a summary of the given text.
        
        Args:
            text: Text to summarize
            length: Summary length ("Brief", "Moderate", or "Detailed")
            
        Returns:
            Summarized text
        """
        # If API is available, use advanced summarization
        if self.model_available:
            return self._ai_summarize(text, length)
        else:
            # Fallback to extractive summarization
            return self._extractive_summarize(text, length)
    
    def _ai_summarize(self, text: str, length: str) -> str:
        """
        Use AI (OpenAI/LangChain) to generate summary.
        
        Args:
            text: Text to summarize
            length: Summary length
            
        Returns:
            AI-generated summary
        """
        try:
            # Try to import langchain
            from langchain.chat_models import ChatOpenAI
            from langchain.chains.summarize import load_summarize_chain
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain.docstore.document import Document
            
            # Configure length parameters
            length_config = {
                "Brief": {"max_tokens": 150, "prompt": "Provide a brief, concise summary in 2-3 sentences."},
                "Moderate": {"max_tokens": 300, "prompt": "Provide a comprehensive summary covering the main points."},
                "Detailed": {"max_tokens": 500, "prompt": "Provide a detailed summary with key insights and important details."}
            }
            
            config = length_config.get(length, length_config["Moderate"])
            
            # Initialize LLM
            llm = ChatOpenAI(
                temperature=0.3,
                model_name="gpt-3.5-turbo",
                max_tokens=config["max_tokens"]
            )
            
            # Split text into chunks if too long
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=4000,
                chunk_overlap=200
            )
            
            chunks = text_splitter.split_text(text)
            docs = [Document(page_content=chunk) for chunk in chunks]
            
            # Use map-reduce chain for long documents
            if len(docs) > 1:
                chain = load_summarize_chain(llm, chain_type="map_reduce")
            else:
                chain = load_summarize_chain(llm, chain_type="stuff")
            
            summary = chain.run(docs)
            
            return summary
        
        except ImportError:
            print("LangChain not available, using extractive summarization")
            return self._extractive_summarize(text, length)
        
        except Exception as e:
            print(f"Error in AI summarization: {e}")
            return self._extractive_summarize(text, length)
    
    def _extractive_summarize(self, text: str, length: str = "Moderate") -> str:
        """
        Generate extractive summary using sentence scoring.
        
        Args:
            text: Text to summarize
            length: Summary length
            
        Returns:
            Extractive summary
        """
        # Clean and split into sentences
        sentences = self._split_into_sentences(text)
        
        if not sentences:
            return "Unable to generate summary."
        
        # Score sentences based on importance
        scored_sentences = self._score_sentences(sentences, text)
        
        # Determine number of sentences based on length
        length_map = {
            "Brief": max(3, len(sentences) // 10),
            "Moderate": max(5, len(sentences) // 5),
            "Detailed": max(8, len(sentences) // 3)
        }
        
        num_sentences = length_map.get(length, length_map["Moderate"])
        num_sentences = min(num_sentences, len(sentences))
        
        # Select top sentences
        top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:num_sentences]
        
        # Sort by original order
        top_sentences = sorted(top_sentences, key=lambda x: x[2])
        
        # Combine into summary
        summary = ' '.join([sent[0] for sent in top_sentences])
        
        return summary
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        return sentences
    
    def _score_sentences(self, sentences: List[str], full_text: str) -> List[tuple]:
        """
        Score sentences based on various factors.
        
        Returns:
            List of tuples (sentence, score, original_index)
        """
        scored = []
        
        # Calculate word frequencies
        words = re.findall(r'\b\w+\b', full_text.lower())
        word_freq = {}
        for word in words:
            if len(word) > 3:  # Ignore short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score each sentence
        for idx, sentence in enumerate(sentences):
            score = 0
            sentence_words = re.findall(r'\b\w+\b', sentence.lower())
            
            # Score based on word frequency
            for word in sentence_words:
                if word in word_freq and len(word) > 3:
                    score += word_freq[word]
            
            # Boost for position (first and last sentences often important)
            if idx < 3:
                score *= 1.5
            elif idx >= len(sentences) - 3:
                score *= 1.3
            
            # Boost for sentence length (moderate length preferred)
            word_count = len(sentence_words)
            if 10 <= word_count <= 30:
                score *= 1.2
            
            scored.append((sentence, score, idx))
        
        return scored
    
    def extract_key_points(self, text: str, num_points: int = 5) -> str:
        """
        Extract key points from text in bullet format.
        
        Args:
            text: Text to extract key points from
            num_points: Number of key points to extract
            
        Returns:
            Formatted key points
        """
        sentences = self._split_into_sentences(text)
        scored_sentences = self._score_sentences(sentences, text)
        
        # Get top sentences
        top_sentences = sorted(scored_sentences, key=lambda x: x[1], reverse=True)[:num_points]
        top_sentences = sorted(top_sentences, key=lambda x: x[2])
        
        # Format as bullet points
        key_points = "**Key Points:**\n\n"
        for i, (sentence, _, _) in enumerate(top_sentences, 1):
            key_points += f"{i}. {sentence}\n\n"
        
        return key_points
    
    def get_summary_stats(self, original: str, summary: str) -> dict:
        """
        Get statistics comparing original and summary.
        
        Returns:
            Dictionary with comparison stats
        """
        return {
            'original_words': len(original.split()),
            'summary_words': len(summary.split()),
            'compression_ratio': round(len(summary) / len(original), 2) if original else 0,
            'original_chars': len(original),
            'summary_chars': len(summary)
        }
