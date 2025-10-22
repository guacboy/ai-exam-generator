from tkinter import *
from util import *

main_window = Tk()
main_window.title("ExamAI")
main_window.geometry("750x850")
main_window.resizable(False, False)
main_window.config(bg=PROGRAM_BG_COLOR)

def menu():
    """
    Main (menu) window of program.
    """
    # title
    title_label = Util(main_window).label()
    title_label.config(text="ExamAI",
                       font=("Arial", 64, "bold"))
    title_label.pack(pady=(100, 0))
    
    # description
    description_label = Util(main_window).label()
    description_label.config(text="Turn notes into practice.",
                             font=("Arial", 24, "normal"))
    description_label.pack(pady=(25, 0))
    
    # view button framework
    view_framework = Util(main_window).frame()
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
    new_note_btn = Util(main_window).button()
    new_note_btn.config(text="New Note",
                        command=lambda: print("new note"))
    new_note_btn.pack(side=BOTTOM,
                      pady=(0, 25))
    
    
if __name__ == "__main__":
    menu()
    main_window.mainloop()