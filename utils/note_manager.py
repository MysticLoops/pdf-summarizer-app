import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class NoteManager:
    """Manages note creation, storage, and export."""
    
    def __init__(self, storage_dir: str = "data/notes"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def create_note(self, title: str, content: str, source: str = "Manual", 
                   note_type: str = "Custom") -> Dict:
        """
        Create a new note.
        
        Args:
            title: Note title
            content: Note content
            source: Source of the note (PDF name, manual, etc.)
            note_type: Type of note
            
        Returns:
            Created note dictionary
        """
        note = {
            'id': self._generate_id(),
            'title': title,
            'content': content,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'source': source,
            'type': note_type
        }
        
        return note
    
    def _generate_id(self) -> str:
        """Generate unique note ID."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def save_note_to_file(self, note: Dict) -> str:
        """
        Save note to JSON file.
        
        Args:
            note: Note dictionary
            
        Returns:
            Path to saved file
        """
        filename = f"note_{note['id']}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(note, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_notes_from_files(self) -> List[Dict]:
        """
        Load all notes from storage directory.
        
        Returns:
            List of note dictionaries
        """
        notes = []
        
        if not os.path.exists(self.storage_dir):
            return notes
        
        for filename in os.listdir(self.storage_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.storage_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        note = json.load(f)
                        notes.append(note)
                except Exception as e:
                    print(f"Error loading note {filename}: {e}")
        
        return sorted(notes, key=lambda x: x['timestamp'], reverse=True)
    
    def export_note(self, note: Dict, format: str = 'txt', output_dir: str = "exports") -> str:
        """
        Export a single note to a file.
        
        Args:
            note: Note dictionary
            format: Export format ('txt', 'md', 'json')
            output_dir: Directory to save exported file
            
        Returns:
            Path to exported file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Sanitize filename
        safe_title = "".join(c for c in note['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title[:50]  # Limit length
        
        if format == 'txt':
            filename = f"{safe_title}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {note['title']}\n")
                f.write(f"Date: {note['timestamp']}\n")
                f.write(f"Source: {note['source']}\n")
                f.write(f"Type: {note['type']}\n")
                f.write("\n" + "="*50 + "\n\n")
                f.write(note['content'])
        
        elif format == 'md':
            filename = f"{safe_title}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {note['title']}\n\n")
                f.write(f"**Date:** {note['timestamp']}  \n")
                f.write(f"**Source:** {note['source']}  \n")
                f.write(f"**Type:** {note['type']}  \n\n")
                f.write("---\n\n")
                f.write(note['content'])
        
        elif format == 'json':
            filename = f"{safe_title}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(note, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def export_all_notes(self, notes: List[Dict], format: str = 'json') -> str:
        """
        Export all notes to a single file.
        
        Args:
            notes: List of note dictionaries
            format: Export format ('json', 'txt', 'md')
            
        Returns:
            Path to exported file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = "exports"
        os.makedirs(output_dir, exist_ok=True)
        
        if format == 'json':
            filename = f"all_notes_{timestamp}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    'export_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_notes': len(notes),
                    'notes': notes
                }, f, indent=2, ensure_ascii=False)
        
        elif format == 'txt':
            filename = f"all_notes_{timestamp}.txt"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"PDF Summarizer Notes Export\n")
                f.write(f"Export Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Total Notes: {len(notes)}\n")
                f.write("\n" + "="*70 + "\n\n")
                
                for i, note in enumerate(notes, 1):
                    f.write(f"Note {i}: {note['title']}\n")
                    f.write(f"Date: {note['timestamp']} | Source: {note['source']}\n")
                    f.write("-"*70 + "\n")
                    f.write(note['content'])
                    f.write("\n\n" + "="*70 + "\n\n")
        
        elif format == 'md':
            filename = f"all_notes_{timestamp}.md"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write("# PDF Summarizer Notes Export\n\n")
                f.write(f"**Export Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
                f.write(f"**Total Notes:** {len(notes)}  \n\n")
                f.write("---\n\n")
                
                for i, note in enumerate(notes, 1):
                    f.write(f"## {i}. {note['title']}\n\n")
                    f.write(f"**Date:** {note['timestamp']}  \n")
                    f.write(f"**Source:** {note['source']}  \n")
                    f.write(f"**Type:** {note['type']}  \n\n")
                    f.write(note['content'])
                    f.write("\n\n---\n\n")
        
        return filepath
    
    def search_notes(self, notes: List[Dict], query: str) -> List[Dict]:
        """
        Search notes by title or content.
        
        Args:
            notes: List of notes to search
            query: Search query
            
        Returns:
            Filtered list of notes
        """
        query_lower = query.lower()
        return [
            note for note in notes
            if query_lower in note['title'].lower() or 
               query_lower in note['content'].lower()
        ]
    
    def filter_by_source(self, notes: List[Dict], source: str) -> List[Dict]:
        """
        Filter notes by source.
        
        Args:
            notes: List of notes
            source: Source to filter by
            
        Returns:
            Filtered notes
        """
        return [note for note in notes if note['source'] == source]
    
    def filter_by_date(self, notes: List[Dict], start_date: str, end_date: str) -> List[Dict]:
        """
        Filter notes by date range.
        
        Args:
            notes: List of notes
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Filtered notes
        """
        filtered = []
        for note in notes:
            note_date = note['timestamp'].split()[0]
            if start_date <= note_date <= end_date:
                filtered.append(note)
        
        return filtered
    
    def get_statistics(self, notes: List[Dict]) -> Dict:
        """
        Get statistics about notes collection.
        
        Args:
            notes: List of notes
            
        Returns:
            Statistics dictionary
        """
        if not notes:
            return {
                'total_notes': 0,
                'total_words': 0,
                'sources': {},
                'types': {}
            }
        
        sources = {}
        types = {}
        total_words = 0
        
        for note in notes:
            # Count sources
            source = note['source']
            sources[source] = sources.get(source, 0) + 1
            
            # Count types
            note_type = note['type']
            types[note_type] = types.get(note_type, 0) + 1
            
            # Count words
            total_words += len(note['content'].split())
        
        return {
            'total_notes': len(notes),
            'total_words': total_words,
            'average_words_per_note': round(total_words / len(notes)),
            'sources': sources,
            'types': types
        }
