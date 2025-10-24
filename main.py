from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk
import PIL.Image as PImage
import json
import os
from datetime import datetime

from util import *
from note import NoteManager

PROGRAM_TITLE = "ExamAI"
DEFAULT_GEOMETRY = "750x850"

note_manager = NoteManager()

class Window:
    def __init__(self, is_main=True):
        if is_main:
            self._window = Tk()
        else:
            self._window = Toplevel()
            
        self._configure_main_window()
    
    def _configure_main_window(self):
        """
        Configures the window settings.
        """
        self._window.title(PROGRAM_TITLE)
        self._window.geometry(DEFAULT_GEOMETRY)
        self._window.resizable(False, False)
        self._window.config(bg=PROGRAM_BG_COLOR)
    
    def create_toplevel(self, title=PROGRAM_TITLE, geometry=DEFAULT_GEOMETRY):
        """
        Create a new Toplevel window.
        """
        new_window = Toplevel(self._window)
        new_window.title(title)
        new_window.geometry(geometry)
        new_window.resizable(False, False)
        new_window.config(bg=PROGRAM_BG_COLOR)
        
        return new_window
    
    def get_window(self):
        return self._window
    
    def run(self):
        self._window.mainloop()

def menu() -> None:
    """
    Main (menu) window of program.
    """
    # title
    title_label = Util(main_window.get_window()).label()
    title_label.config(text=PROGRAM_TITLE,
                       font=("Arial", 64, "bold"))
    title_label.pack(pady=(100, 0))
    
    # description
    description_label = Util(main_window.get_window()).label()
    description_label.config(text="Turn notes into practice.",
                             font=("Arial", 24, "normal"))
    description_label.pack(pady=(25, 0))
    
    # view button framework
    view_framework = Util(main_window.get_window()).frame()
    view_framework.pack(side=BOTTOM,
                        pady=(0, 100))
    
        # view notes button
    view_notes_btn = Util(view_framework).button()
    view_notes_btn.config(text="View Notes",
                          command=lambda: print("view notes"))
    view_notes_btn.pack(side=LEFT)
    
        # view exams button
    view_exams_btn = Util(view_framework).button()
    view_exams_btn.config(text="View Exams",
                          command=lambda: print("view exams"))
    view_exams_btn.pack(side=LEFT,
                        padx=(25, 0))
    
    # new note button
    new_note_btn = Util(main_window.get_window()).button()
    new_note_btn.config(text="New Note",
                        command=lambda: new_note())
    new_note_btn.pack(side=BOTTOM,
                      pady=(0, 25))

def new_note() -> None:
    """
    Window to input new notes.
    """
    # creates a new window
    new_note_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - New Note")
    
    # generate unique ID for this note session
    note_id = f"note_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # note information frame
    note_frame = Util(new_note_window).frame()
    note_frame.pack()
    
        # title text
    title_text = Util(note_frame).text()
    title_text.config(bg=PROGRAM_BG_COLOR,
                      font=("Arial", 20, "normal"),
                      width=30,
                      height=1)
    title_text.insert(INSERT, "Untitled")
    title_text.pack(side=LEFT,
                    padx=(0, 135))
    
        # note's current status
    note_status_label = Util(note_frame).label()
    note_status_label.config(text="Notes saved.",
                             font=("Arial", 12, "normal"))
    note_status_label.pack(side=RIGHT)
    
    # note text
    note_text = Util(new_note_window).text()
    note_text.config(bg="#1E1E1E",
                     font=("Arial", 12, "normal"),
                     width=75,
                     height=40)
    note_text.pack()
    
        # add placeholder
    placeholder_text = "This is where you'll enter your notes.\n\n" \
        "You can also upload files containing text to which it will appear here.\n\n" \
        "When you're finished, click 'Generate' to create a multiple-choice exam pertaining your notes.\n\n" \
        "Don't worry, all of your changes will be automatically saved."
    note_text.insert("1.0", placeholder_text)
    note_text.config(fg="gray")

    def clear_placeholder(event):
        if note_text.get("1.0", "end-1c") == placeholder_text:
            note_text.delete("1.0", "end")
            note_text.config(fg="white")

    def add_placeholder_if_empty(event):
        if not note_text.get("1.0", "end-1c").strip():
            note_text.insert("1.0", placeholder_text)
            note_text.config(fg="gray")

    note_text.bind("<FocusIn>", clear_placeholder)
    note_text.bind("<FocusOut>", add_placeholder_if_empty)
    
    # note option frame
    note_option_frame = Util(new_note_window).frame()
    note_option_frame.pack(side=BOTTOM)

        # load and resize image
    pil_image = PImage.open("./assets/upload_icon.png")
    pil_image = pil_image.resize((64, 64))  # reize
    upload_icon = ImageTk.PhotoImage(pil_image)
        # upload button
    upload_btn = Util(new_note_window).button()
    upload_btn.config(image=upload_icon,
                      command=lambda: upload_file_window())
    upload_btn.image = upload_icon  # keeps reference
    upload_btn.pack(side=LEFT,
                    padx=(10, 0))
    
    def upload_file_window() -> None:
        """
        Uploads files into the text area.
        """
        # creates a new window
        upload_file_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - Upload Note",
                                                         "500x250")
        
        # upload option frame
        upload_options_frame = Util(upload_file_window).frame()
        upload_options_frame.pack(side=TOP,
                                  pady=(25, 0))
        
            # load and resize image
        pil_image = PImage.open("./assets/upload_icon.png")
        pil_image = pil_image.resize((64, 64))  # reize
        upload_icon = ImageTk.PhotoImage(pil_image)
            # upload image
        upload_label = Util(upload_options_frame).label()
        upload_label.config(image=upload_icon)
        upload_btn.image = upload_icon  # keeps reference
        upload_label.pack()
        
            # upload instruction label
        upload_instruction_label = Util(upload_options_frame).label()
        upload_instruction_label.config(text="Choose a file or drag & drop here",
                                        font=("Arial", 20, "normal"))
        upload_instruction_label.pack()
            
            # upload sub-instruction label
        upload_sub_instruction_label = Util(upload_options_frame).label()
        upload_sub_instruction_label.config(text="JPG, PNG, TXT, and DOCX formats, up to 50 MB",
                                            font=("Arial", 12, "normal"),
                                            fg="#D9D9D9")
        upload_sub_instruction_label.pack()
        
            # browse files button
        browse_file_btn = Util(upload_options_frame).button()
        browse_file_btn.config(text="Browse File",
                               font=("Arial", 12, "normal"),
                               padx=10,
                               command=lambda: upload_file())
        browse_file_btn.pack(pady=(10, 0))
        
        def upload_file() -> None:
            # supported file types
            file_types = [
                ("Text files", "*.txt"),
                ("JPG files", "*.jpg"),
                ("PNG files", "*.png"),
                ("DOCX files", "*.docx")
            ]
            
            # open file dialog
            file_path = filedialog.askopenfilename(
                title="Select a file to upload",
                filetypes=file_types
            )
            
            # if user selected a file
            if file_path:
                try:
                    # get file size to check if it's too large
                    file_size = os.path.getsize(file_path)
                    max_size = 5 * 1024 * 1024  # 5MB limit
                    
                    if file_size > max_size:
                        messagebox.showwarning(
                            "File Too Large",
                            f"The selected file is too large ({file_size // 1024} KB).\n"
                            f"Please select a file smaller than 5MB."
                        )
                        return
                    
                    # read the file content
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    # clear any existing placeholder
                    current_content = note_text.get("1.0", "end-1c")
                    if current_content == placeholder_text:
                        note_text.delete("1.0", "end")
                        note_text.config(fg="white")
                    
                    # insert file content at cursor position or replace all
                    if note_text.get("1.0", "end-1c").strip():  # if there's existing content
                        # ask user if they want to replace or append
                        choice = messagebox.askyesnocancel(
                            "Insert Content",
                            "Would you like to replace the current content?\n\n"
                            "Yes - Replace all content\n"
                            "No - Append to current content\n"
                            "Cancel - Do nothing"
                        )
                        
                        if choice is None:  # cancel
                            return
                        elif choice:  # yes - replace all
                            note_text.delete("1.0", "end")
                            note_text.insert("1.0", content)
                        else:  # no - append
                            note_text.insert("end", f"\n\n--- Content from {os.path.basename(file_path)} ---\n")
                            note_text.insert("end", content)
                    else:
                        # just insert if text area is empty
                        note_text.insert("1.0", content)
                    
                    # show success message
                    messagebox.showinfo(
                        "File Uploaded",
                        f"Successfully loaded: {os.path.basename(file_path)}"
                    )
                    
                except UnicodeDecodeError:
                    # try with different encoding if UTF-8 fails
                    try:
                        with open(file_path, 'r', encoding='latin-1') as file:
                            content = file.read()
                        
                        # insert content (similar to above)
                        current_content = note_text.get("1.0", "end-1c")
                        if current_content == placeholder_text:
                            note_text.delete("1.0", "end")
                            note_text.config(fg="white")
                        
                        note_text.insert("end", f"\n\n--- Content from {os.path.basename(file_path)} ---\n")
                        note_text.insert("end", content)
                        
                        messagebox.showinfo(
                            "File Uploaded",
                            f"Successfully loaded: {os.path.basename(file_path)}\n"
                            f"(Note: Used fallback encoding)"
                        )
                        
                    except Exception as e:
                        messagebox.showerror(
                            "Error Reading File",
                            f"Could not read the file: {str(e)}"
                        )
                
                except Exception as e:
                    messagebox.showerror(
                        "Error",
                        f"An error occurred while reading the file: {str(e)}"
                    )
    
        # load and resize image
    pil_image = PImage.open("./assets/generate_exam_icon.png")
    pil_image = pil_image.resize((64, 64))  # reize
    generate_exam_icon = ImageTk.PhotoImage(pil_image)
        # generate button
    generate_exam_btn = Util(new_note_window).button()
    generate_exam_btn.config(text="Generate",
                             image=generate_exam_icon,
                             compound=RIGHT,
                             padx=10,
                             pady=0,
                             command=lambda: print("generate"))
    generate_exam_btn.image = generate_exam_icon
    generate_exam_btn.pack(side=RIGHT,
                           padx=(0, 10))
    
    # auto-save function using NoteManager
    def auto_save():
        title = title_text.get("1.0", "end-1c").strip() or "Untitled"
        content = note_text.get("1.0", "end-1c")
        
        if note_manager.save_note(note_id, title, content, placeholder_text):
            current_time = datetime.now().strftime("%H:%M:%S")
            note_status_label.config(text=f"Auto-saved at {current_time}")
        
        new_note_window.after(30000, auto_save)  # every 30 seconds
    
    # start auto-save
    auto_save()
    
    # save on close
    def on_closing():
        title = title_text.get("1.0", "end-1c").strip() or "Untitled"
        content = note_text.get("1.0", "end-1c")
        note_manager.save_note(note_id, title, content, placeholder_text)
        new_note_window.destroy()
    
    new_note_window.protocol("WM_DELETE_WINDOW", on_closing)



if __name__ == "__main__":
    main_window = Window()
    menu()
    main_window.run()