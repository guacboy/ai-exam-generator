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
                          command=lambda: view_notes())
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

def new_note(note_id=None) -> None:
    """
    Window to input new notes.
    """
    # creates a new window
    new_note_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - New Note")
    
    # load notes data
    notes_data = {}
    try:
        with open("notes_data/notes.json", "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    
    # initialize variables
    title_content = "Untitled"
    note_content = ""
    
    # if note_id is provided and exists, load the data
    if note_id and note_id in notes_data:
        note_data = notes_data[note_id]
        title_content = note_data.get("title", "Untitled")
        note_content = note_data.get("content", "")
    else:
        # generate unique ID for new note session
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
    title_text.insert(INSERT, title_content)
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
    
    if note_content.strip():  # If there's existing content
        note_text.insert(INSERT, note_content)
        note_text.config(fg="white")
    else:
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
    pil_image = pil_image.resize((64, 64))  # resize
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
        pil_image = pil_image.resize((64, 64))  # resize
        upload_icon = ImageTk.PhotoImage(pil_image)
            # upload image
        upload_label = Util(upload_options_frame).label()
        upload_label.config(image=upload_icon)
        upload_label.image = upload_icon  # keeps reference
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
    pil_image = pil_image.resize((64, 64))  # resize
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
    
    def save_note():
        """
        Save the note (new or existing).
        """
        title = title_text.get("1.0", "end-1c").strip() or "Untitled"
        content = note_text.get("1.0", "end-1c")
        
        # don't save if it's just placeholder text
        if content == placeholder_text:
            return
        
        # load current notes data
        try:
            with open("notes_data/notes.json", "r", encoding="utf-8") as f:
                all_notes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            all_notes = {}
        
        # update or create note
        all_notes[note_id] = {
            'title': title,
            'content': content,
            'last_modified': datetime.now().isoformat(),
            'created': all_notes.get(note_id, {}).get('created', datetime.now().isoformat())
        }
        
        # save back to file
        try:
            with open("notes_data/notes.json", "w", encoding="utf-8") as f:
                json.dump(all_notes, f, indent=2, ensure_ascii=False)
            
            # update status
            current_time = datetime.now().strftime("%H:%M:%S")
            note_status_label.config(text=f"Saved at {current_time}")
            
        except Exception as e:
            note_status_label.config(text=f"Save failed: {str(e)}")
    
    # auto-save
    def auto_save():
        save_note()
        new_note_window.after(30000, auto_save)  # save every 30 seconds
    
    auto_save()
    
    # save on close
    def on_closing():
        save_note()
        new_note_window.destroy()
    
    new_note_window.protocol("WM_DELETE_WINDOW", on_closing)

def view_notes() -> None:
    view_notes_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - View Notes")
    
    # search notes frame
    search_notes_frame = Util(view_notes_window).frame()
    search_notes_frame.pack(side=TOP,
                            pady=(0, 5))
    
        # load and resize image
    pil_image = PImage.open("./assets/search_icon.png")
    pil_image = pil_image.resize((32, 32))  # resize
    search_icon = ImageTk.PhotoImage(pil_image)
        # upload image
    search_label = Util(search_notes_frame).label()
    search_label.config(image=search_icon)
    search_label.image = search_icon  # keeps reference
    search_label.pack(side=LEFT)
    
        # search notes text
    search_notes_text = Util(search_notes_frame).text()
    search_notes_text.config(font=("Arial", 16, "normal"),
                             bg="#4D4C4C",
                             height=1)
    search_notes_text.pack(side=LEFT)
    
        # add placeholder
    placeholder_text = "Search..."
    search_notes_text.insert("1.0", placeholder_text)
    search_notes_text.config(fg="gray")

    def clear_placeholder(event):
        if search_notes_text.get("1.0", "end-1c") == placeholder_text:
            search_notes_text.delete("1.0", "end")
            search_notes_text.config(fg="white")

    def add_placeholder_if_empty(event):
        if not search_notes_text.get("1.0", "end-1c").strip():
            search_notes_text.insert("1.0", placeholder_text)
            search_notes_text.config(fg="gray")

    search_notes_text.bind("<FocusIn>", clear_placeholder)
    search_notes_text.bind("<FocusOut>", add_placeholder_if_empty)
    
    # load notes data
    try:
        with open("notes_data/notes.json", "r", encoding="utf-8") as f:
            notes_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        notes_data = {}
        
    # notes list frame
    notes_frame = Util(view_notes_window).frame()
    notes_frame.pack(side=LEFT,
                     anchor=NW,
                     fill="x",
                     expand=True,
                     padx=10,
                     pady=(0, 5))
    
    if not notes_data:
        # no notes message
        no_notes_label = Util(notes_frame).label()
        no_notes_label.config(text="No notes found. Create a new note to get started!",
                             font=("Arial", 12, "normal"))
        no_notes_label.pack(pady=50)
    else:
        # display each note
        for note_id, note_data in notes_data.items():
            # note container frame for the entire note row
            note_container = Util(notes_frame).frame()
            note_container.pack(fill="x",
                                pady=5)
            
            # individual note frame
            note_frame = Util(note_container).frame()
            note_frame.config(bg="#4D4C4C")
            note_frame.pack(side=LEFT,
                            fill="x",
                            expand=True)
            
                # last modified
            last_modified = note_data.get("last_modified", "")
            if last_modified:
                try:
                    mod_date = datetime.fromisoformat(last_modified)
                    last_modified = mod_date.strftime("%m/%d/%Y %H:%M")
                except ValueError:
                    last_modified = "Unknown"
            
                # note title label
            title = note_data.get("title", "Untitled")
            note_title_label = Util(note_frame).label()
            note_title_label.config(text=title,
                                    font=("Arial", 12, "bold"),
                                    bg="#4D4C4C")
            note_title_label.pack(anchor=W)

                # note last modified label
            note_last_modified_label = Util(note_frame).label()
            note_last_modified_label.config(text=f"Last Modified: {last_modified}",
                                            font=("Arial", 12, "normal"),
                                            bg="#4D4C4C")
            note_last_modified_label.pack(anchor=W)
            
            # separate frame for buttons on the right
            button_frame = Util(note_container).frame()
            button_frame.pack(side=RIGHT,
                              padx=(10, 0))
            
                # load and resize image
            pil_image = PImage.open("./assets/edit_icon.png")
            pil_image = pil_image.resize((42, 42))  # resize
            edit_icon = ImageTk.PhotoImage(pil_image)
                # edit button
            edit_btn = Util(button_frame).button()
            edit_btn.config(image=edit_icon,
                            command=lambda nid=note_id: open_note(nid))
            edit_btn.image = edit_icon  # keeps reference
            edit_btn.pack(side=LEFT,
                          padx=(0, 10))
            
                # load and resize image
            pil_image = PImage.open("./assets/delete_icon.png")
            pil_image = pil_image.resize((42, 42))  # resize
            delete_icon = ImageTk.PhotoImage(pil_image)
                # delete button
            delete_btn = Util(button_frame).button()
            delete_btn.config(image=delete_icon,
                              command=lambda nid=note_id, nt=title: confirm_delete(nid, nt))
            delete_btn.image = delete_icon  # keeps reference
            delete_btn.pack(side=LEFT)
            
        def confirm_delete(note_id, note_title):
            """
            Show confirmation dialog before deleting a note.
            """
            response = messagebox.askquestion(
                "Confirm Delete",
                f"Are you sure you want to delete\n'{note_title}'?\n\nThis cannot be undone.",
                icon='warning',
            )
            
            if response == 'yes':
                delete_note(note_id)

        def delete_note(note_id):
            """
            Actually delete the note from the JSON file and refresh the view.
            """
            try:
                # load current notes data
                with open("notes_data/notes.json", "r", encoding="utf-8") as f:
                    notes_data = json.load(f)
                
                # remove the note
                if note_id in notes_data:
                    del notes_data[note_id]
                    
                    # save updated data
                    with open("notes_data/notes.json", "w", encoding="utf-8") as f:
                        json.dump(notes_data, f, indent=2, ensure_ascii=False)
                    
                    # show success message
                    messagebox.showinfo("Success", "Note deleted successfully.")
                    
                    # refresh the view notes window
                    refresh_notes_view()
                else:
                    messagebox.showerror("Error", "Note not found.")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete note: {str(e)}")

        def refresh_notes_view():
            """
            Refresh the view notes window to reflect changes.
            """
            # close the current view notes window
            view_notes_window.destroy()
            # reopen the view notes window
            view_notes()
            
        def open_note(note_id):
            """
            Open an existing note in the editor.
            """
            view_notes_window.destroy()  # close the view window
            new_note(note_id)  # open the note editor with the specific note ID

if __name__ == "__main__":
    main_window = Window()
    menu()
    main_window.run()