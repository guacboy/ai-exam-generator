import os
import json
from datetime import datetime

class NoteManager:
    def __init__(self, data_dir="notes_data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.notes_file = os.path.join(data_dir, "notes.json")
        self.notes = self.load_notes()
    
    def load_notes(self):
        """
        Load all notes from JSON file
        """
        if os.path.exists(self.notes_file):
            try:
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def generate_note_id(self):
        """
        Generate a unique note ID using the microservice
        """
        # import the function from main to avoid circular imports
        from main import generate_unique_id
        return generate_unique_id()
    
    def save_note(self, note_id, title, content, placeholder_text):
        """
        Save a note to JSON file
        """
        if content == placeholder_text:
            return False
        
        self.notes[note_id] = {
            'title': title,
            'content': content,
            'last_modified': datetime.now().isoformat(),
            'created': self.notes.get(note_id, {}).get('created', datetime.now().isoformat())
        }
        
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=2, ensure_ascii=False)
            return True
        except:
            return False
    
    def get_all_notes(self):
        """
        Get all saved notes
        """
        return self.notes
    
    def delete_note(self, note_id):
        """
        Delete a note
        """
        if note_id in self.notes:
            del self.notes[note_id]
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, indent=2, ensure_ascii=False)
            return True
        return False