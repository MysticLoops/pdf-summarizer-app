from typing import List, Dict, Optional
from datetime import datetime

class Database:
    """Handles MongoDB operations for persistent storage."""
    
    def __init__(self):
        self.client = None
        self.db = None
        self.notes_collection = None
        self.connected = False
        self._try_connect()
    
    def _try_connect(self):
        """Attempt to connect to MongoDB."""
        try:
            from pymongo import MongoClient
            
            # Try to connect to local MongoDB
            self.client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)
            
            # Test connection
            self.client.server_info()
            
            # Set database and collection
            self.db = self.client['pdf_summarizer']
            self.notes_collection = self.db['notes']
            
            self.connected = True
            print("✅ Connected to MongoDB")
        
        except ImportError:
            print("⚠️ pymongo not installed. Using local storage only.")
            self.connected = False
        
        except Exception as e:
            print(f"⚠️ Could not connect to MongoDB: {e}")
            print("Using local storage only.")
            self.connected = False
    
    def test_connection(self, uri: str = None, db_name: str = "pdf_summarizer") -> bool:
        """
        Test database connection.
        
        Args:
            uri: MongoDB connection URI
            db_name: Database name
            
        Returns:
            True if connection successful
        """
        try:
            from pymongo import MongoClient
            
            uri = uri or 'mongodb://localhost:27017/'
            client = MongoClient(uri, serverSelectionTimeoutMS=2000)
            client.server_info()
            
            self.client = client
            self.db = client[db_name]
            self.notes_collection = self.db['notes']
            self.connected = True
            
            return True
        
        except Exception as e:
            print(f"Connection test failed: {e}")
            return False
    
    def save_note(self, note: Dict) -> bool:
        """
        Save a note to the database.
        
        Args:
            note: Note dictionary
            
        Returns:
            True if successful
        """
        if not self.connected:
            return False
        
        try:
            # Add MongoDB timestamp
            note['mongodb_timestamp'] = datetime.now()
            
            # Insert or update
            result = self.notes_collection.update_one(
                {'id': note['id']},
                {'$set': note},
                upsert=True
            )
            
            return True
        
        except Exception as e:
            print(f"Error saving note to database: {e}")
            return False
    
    def get_note(self, note_id: str) -> Optional[Dict]:
        """
        Retrieve a note by ID.
        
        Args:
            note_id: Note ID
            
        Returns:
            Note dictionary or None
        """
        if not self.connected:
            return None
        
        try:
            note = self.notes_collection.find_one({'id': note_id})
            
            if note:
                # Remove MongoDB _id field
                note.pop('_id', None)
                note.pop('mongodb_timestamp', None)
            
            return note
        
        except Exception as e:
            print(f"Error retrieving note: {e}")
            return None
    
    def get_all_notes(self) -> List[Dict]:
        """
        Retrieve all notes from database.
        
        Returns:
            List of note dictionaries
        """
        if not self.connected:
            return []
        
        try:
            notes = list(self.notes_collection.find())
            
            # Clean up MongoDB fields
            for note in notes:
                note.pop('_id', None)
                note.pop('mongodb_timestamp', None)
            
            return sorted(notes, key=lambda x: x.get('timestamp', ''), reverse=True)
        
        except Exception as e:
            print(f"Error retrieving notes: {e}")
            return []
    
    def delete_note(self, note_id: str) -> bool:
        """
        Delete a note from database.
        
        Args:
            note_id: Note ID to delete
            
        Returns:
            True if successful
        """
        if not self.connected:
            return False
        
        try:
            result = self.notes_collection.delete_one({'id': note_id})
            return result.deleted_count > 0
        
        except Exception as e:
            print(f"Error deleting note: {e}")
            return False
    
    def search_notes(self, query: str) -> List[Dict]:
        """
        Search notes in database.
        
        Args:
            query: Search query
            
        Returns:
            List of matching notes
        """
        if not self.connected:
            return []
        
        try:
            # Create text index if it doesn't exist
            try:
                self.notes_collection.create_index([
                    ('title', 'text'),
                    ('content', 'text')
                ])
            except:
                pass  # Index might already exist
            
            # Search using text index
            notes = list(self.notes_collection.find(
                {'$text': {'$search': query}}
            ))
            
            # Clean up MongoDB fields
            for note in notes:
                note.pop('_id', None)
                note.pop('mongodb_timestamp', None)
            
            return notes
        
        except Exception as e:
            print(f"Error searching notes: {e}")
            return []
    
    def filter_notes(self, filters: Dict) -> List[Dict]:
        """
        Filter notes by criteria.
        
        Args:
            filters: Dictionary of filter criteria
            
        Returns:
            List of filtered notes
        """
        if not self.connected:
            return []
        
        try:
            notes = list(self.notes_collection.find(filters))
            
            # Clean up MongoDB fields
            for note in notes:
                note.pop('_id', None)
                note.pop('mongodb_timestamp', None)
            
            return notes
        
        except Exception as e:
            print(f"Error filtering notes: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """
        Get database statistics.
        
        Returns:
            Statistics dictionary
        """
        if not self.connected:
            return {'connected': False}
        
        try:
            total_notes = self.notes_collection.count_documents({})
            
            # Aggregate by source
            sources_pipeline = [
                {'$group': {
                    '_id': '$source',
                    'count': {'$sum': 1}
                }}
            ]
            sources = list(self.notes_collection.aggregate(sources_pipeline))
            
            # Aggregate by type
            types_pipeline = [
                {'$group': {
                    '_id': '$type',
                    'count': {'$sum': 1}
                }}
            ]
            types = list(self.notes_collection.aggregate(types_pipeline))
            
            return {
                'connected': True,
                'total_notes': total_notes,
                'sources': {s['_id']: s['count'] for s in sources},
                'types': {t['_id']: t['count'] for t in types}
            }
        
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {'connected': False, 'error': str(e)}
    
    def backup_database(self, output_file: str = "backup.json") -> bool:
        """
        Backup all notes to JSON file.
        
        Args:
            output_file: Output file path
            
        Returns:
            True if successful
        """
        if not self.connected:
            return False
        
        try:
            import json
            
            notes = self.get_all_notes()
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'backup_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_notes': len(notes),
                    'notes': notes
                }, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error backing up database: {e}")
            return False
    
    def restore_from_backup(self, backup_file: str) -> bool:
        """
        Restore notes from backup file.
        
        Args:
            backup_file: Path to backup file
            
        Returns:
            True if successful
        """
        if not self.connected:
            return False
        
        try:
            import json
            
            with open(backup_file, 'r', encoding='utf-8') as f:
                backup_data = json.load(f)
            
            notes = backup_data.get('notes', [])
            
            for note in notes:
                self.save_note(note)
            
            return True
        
        except Exception as e:
            print(f"Error restoring from backup: {e}")
            return False
    
    def close(self):
        """Close database connection."""
        if self.client:
            self.client.close()
            print("Database connection closed")
