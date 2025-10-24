from tkinter import *
from PIL import ImageTk
import PIL.Image as PImage

from util import *

PROGRAM_TITLE = "ExamAI"
DEFAULT_GEOMETRY = "750x850"

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
                      command=lambda: print("upload"))
    upload_btn.image = upload_icon  # keeps reference
    upload_btn.pack(side=LEFT,
                    padx=(10, 0))
    
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
    
def upload_file() -> None:
    """
    Uploads files into the text area.
    """
    pass
    
if __name__ == "__main__":
    main_window = Window()
    menu()
    main_window.run()