import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from datetime import datetime

class SuggestionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Suggestion Box")
        self.root.geometry("500x400")
        
        # initialize suggestions array
        self.suggestions = []
        
        self.setup_ui()
        
    def setup_ui(self):
        """
        Setup the user interface.
        """
        # main frame
        main_frame = tk.Frame(self.root,
                              padx=20,
                              pady=20)
        main_frame.pack(fill=tk.BOTH,
                        expand=True)
        
        # title
        title_label = tk.Label(main_frame,
                               text="Submit Your Suggestion", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # suggestion entry
        entry_label = tk.Label(main_frame,
                               text="Enter your suggestion:", 
                               font=("Arial", 12))
        entry_label.pack(anchor="w",
                         pady=(20, 5))
        
        self.entry_box = tk.Text(main_frame,
                                 height=8,
                                 width=50, 
                                 font=("Arial", 10))
        self.entry_box.pack(fill=tk.BOTH,
                            expand=True,
                            pady=5)
        
        # attached file info
        self.file_label = tk.Label(main_frame,
                                   text="No file attached", 
                                   fg="gray",
                                   font=("Arial", 9))
        self.file_label.pack(anchor="w",
                             pady=(5, 0))
        
        # button frame
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X,
                          pady=20)
        
        # attach file button
        self.attach_btn = tk.Button(button_frame,
                                    text="Attach File", 
                                    command=self.attach_file,
                                    font=("Arial", 10))
        self.attach_btn.pack(side=tk.LEFT,
                             padx=(0, 10))
        
        # submit button
        self.submit_btn = tk.Button(button_frame, text="Submit Suggestion", 
                                    command=self.submit_suggestion,
                                    font=("Arial", 10, "bold"),
                                    bg="#4CAF50",
                                    fg="white")
        self.submit_btn.pack(side=tk.RIGHT)
        
        # initialize attached file
        self.attached_file = None
        
    def attach_file(self):
        """
        Open file picker to attach an image or document.
        """
        file_types = [
            ("All supported files", "*.jpg *.jpeg *.png *.pdf *.doc *.docx *.txt"),
            ("Images", "*.jpg *.jpeg *.png"),
            ("Documents", "*.pdf *.doc *.docx *.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select a file to attach",
            filetypes=file_types
        )
        
        if filename:
            self.attached_file = filename
            file_name = os.path.basename(filename)
            self.file_label.config(text=f"Attached: {file_name}", fg="green")
    
    def submit_suggestion(self):
        """
        Submit the suggestion to the file.
        """
        suggestion_text = self.entry_box.get("1.0", tk.END).strip()
        
        if not suggestion_text:
            messagebox.showwarning("Warning", "Please enter a suggestion before submitting.")
            return
        
        try:
            # create suggestion object
            suggestion_data = {
                "suggestion": suggestion_text,
                "timestamp": datetime.now().isoformat(),
                "has_attachment": self.attached_file is not None,
                "attachment_path": self.attached_file if self.attached_file else None
            }
            
            # add to suggestions array
            self.suggestions.append(suggestion_data)
            
            # write to suggestion.txt
            with open("suggestion.txt", "a", encoding="utf-8") as f:
                f.write(json.dumps(suggestion_data) + "\n")
            
            # show success message
            messagebox.showinfo("Success", "Your suggestion has been received and will be reviewed.")
            
            # clear the form
            self.entry_box.delete("1.0", tk.END)
            self.file_label.config(text="No file attached", fg="gray")
            self.attached_file = None
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to submit suggestion: {str(e)}")

def main():
    """
    Main function to run the suggestion app.
    """
    root = tk.Tk()
    app = SuggestionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()