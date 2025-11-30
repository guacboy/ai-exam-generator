import json
import time
import os
from datetime import datetime
import threading

class SuggestionReceiver:
    def __init__(self):
        self.suggestion_file = "suggestion.txt"
        self.database_file = "data.json"
        self.processed_suggestions = set()
        self.ensure_files_exist()
        
    def ensure_files_exist(self):
        """
        Ensure both suggestion.txt and data.json files exist and are valid.
        """
        # ensure suggestion.txt exists
        if not os.path.exists(self.suggestion_file):
            with open(self.suggestion_file, 'w', encoding='utf-8') as f:
                pass # create empty file
        
        # ensure data.json exists with valid JSON structure
        if not os.path.exists(self.database_file):
            self.write_database([])
        else:
            # validate existing data.json
            try:
                with open(self.database_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if not content: # if file is empty
                        self.write_database([])
                    else:
                        json.loads(content) # test if valid JSON
            except (json.JSONDecodeError, ValueError):
                # if invalid JSON, reset the file
                print("warning: data.json contains invalid JSON, resetting file...")
                self.write_database([])
    
    def write_database(self, data):
        """
        Safely write data to the database file.
        """
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"error writing to database: {e}")
    
    def read_database(self):
        """
        Safely read data from the database file.
        """
        try:
            with open(self.database_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"error reading database (resetting file): {e}")
            self.write_database([])
            return []
        except Exception as e:
            print(f"unexpected error reading database: {e}")
            return []
    
    def read_suggestions(self):
        """
        Read new suggestions from the suggestion file.
        """
        if not os.path.exists(self.suggestion_file):
            return []
        
        try:
            with open(self.suggestion_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            suggestions = []
            for line in lines:
                line = line.strip()
                if line and line not in self.processed_suggestions:
                    try:
                        suggestion_data = json.loads(line)
                        suggestions.append(suggestion_data)
                        self.processed_suggestions.add(line)
                    except json.JSONDecodeError:
                        print(f"invalid JSON format in suggestion file: {line}")
            
            return suggestions
        except Exception as e:
            print(f"error reading suggestions: {e}")
            return []
    
    def add_to_database(self, suggestion_data):
        """
        Add suggestion to the JSON database.
        """
        try:
            # read existing data safely
            data = self.read_database()
            
            # create database entry
            db_entry = {
                "id": len(data) + 1,
                "suggestion": suggestion_data["suggestion"],
                "date_added": datetime.now().isoformat(),
                "status": "new",
                "has_attachment": suggestion_data.get("has_attachment", False),
                "attachment_path": suggestion_data.get("attachment_path"),
                "submission_timestamp": suggestion_data.get("timestamp")
            }
            
            # add to database
            data.append(db_entry)
            
            # write back to file
            self.write_database(data)
            
            print(f"added suggestion to database: {db_entry['id']}")
            return db_entry
            
        except Exception as e:
            print(f"error adding to database: {e}")
            return None
    
    def display_latest_additions(self):
        """
        Display the frequently updated list of database additions
        """
        try:
            data = self.read_database()
            
            # get recent additions (last 10)
            recent = data[-10:] if data else []
            recent.reverse()
            
            print("\n" + "="*50)
            print("latest suggestions in database")
            print("="*50)
            
            if not recent:
                print("no suggestions in database yet")
                print("="*50)
                return
            
            for item in recent:
                status_color = {
                    "new": "🟢",
                    "reviewed": "🔵", 
                    "declined": "🔴"
                }.get(item["status"], "⚪")
                
                print(f"{status_color} id: {item['id']} | status: {item['status']:8} | date: {item['date_added'][:19]}")
                suggestion_preview = item['suggestion'][:80] + ('...' if len(item['suggestion']) > 80 else '')
                print(f"   suggestion: {suggestion_preview}")
                if item['has_attachment']:
                    print(f"   📎 attachment: {item.get('attachment_path', 'n/a')}")
                print("-" * 50)
                
        except Exception as e:
            print(f"error displaying database: {e}")
    
    def process_suggestions(self):
        """
        Main processing loop.
        """
        print("suggestion receiver started...")
        print("monitoring for new suggestions...")
        
        last_display_time = 0
        display_interval = 5 # seconds
        
        while True:
            try:
                # read new suggestions
                new_suggestions = self.read_suggestions()
                
                # process each new suggestion
                for suggestion in new_suggestions:
                    print(f"processing new suggestion: {suggestion['suggestion'][:50]}...")
                    result = self.add_to_database(suggestion)
                    if result:
                        print(f"successfully processed suggestion id: {result['id']}")
                    else:
                        print("failed to process suggestion")
                
                # display updates periodically
                current_time = time.time()
                if current_time - last_display_time >= display_interval:
                    self.display_latest_additions()
                    last_display_time = current_time
                
                time.sleep(1)  # check every second
                
            except KeyboardInterrupt:
                print("\nshutting down suggestion receiver...")
                break
            except Exception as e:
                print(f"error in processing loop: {e}")
                time.sleep(5)

def main():
    """
    Main function to run the receiver service.
    """
    receiver = SuggestionReceiver()
    receiver.process_suggestions()

if __name__ == "__main__":
    main()