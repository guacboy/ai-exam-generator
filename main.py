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
        with open("data/notes.json", "r", encoding="utf-8") as f:
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
                             command=lambda: amount_of_questions())
    generate_exam_btn.image = generate_exam_icon
    generate_exam_btn.pack(side=RIGHT,
                           padx=(0, 10))
    
    def amount_of_questions() -> int:
        """
        Prompt user for the number of questions to generate.
        Returns the selected number of questions.
        """
        # creates a new window
        exam_options_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - Exam Options",
                                                         "500x250")
        
        # initialize the number of questions
        question_count = IntVar(value=10)  # default to 10 questions
        
        # title label
        title_label = Util(exam_options_window).label()
        title_label.config(text="Amount of Questions to Appear",
                           font=("Arial", 16, "bold"))
        title_label.pack(pady=(50, 10))
        
        # number input frame
        number_frame = Util(exam_options_window).frame()
        number_frame.pack(pady=(0, 20))
        
        # left arrow (decrease)
        left_arrow_label = Util(number_frame).label()
        left_arrow_label.config(text="<",
                                font=("Arial", 24, "bold"),
                                fg="#FFFFFF",
                                cursor="hand2")
        left_arrow_label.pack(side=LEFT,
                              padx=20)
        
        # number display
        number_entry = Entry(number_frame,
                             textvariable=question_count,
                             font=("Arial", 20, "bold"),
                             width=4,
                             bg="#4D4C4C",
                             fg="white",
                             relief="solid",
                             bd=1,
                             justify="center")
        number_entry.pack(side=LEFT)
        
        # right arrow (increase)
        right_arrow_label = Util(number_frame).label()
        right_arrow_label.config(text=">",
                                font=("Arial", 24, "bold"),
                                fg="#FFFFFF",
                                cursor="hand2")
        right_arrow_label.pack(side=LEFT,
                               padx=20)
        
        # function to increase number
        def increase_number(event=None):
            current = question_count.get()
            if current < 30:  # maximum 30 questions
                question_count.set(current + 1)
        
        # function to decrease number
        def decrease_number(event=None):
            current = question_count.get()
            if current > 1:  # minimum 1 question
                question_count.set(current - 1)
        
        # validate function for entry
        def validate_entry(input):
            if input.isdigit() or input == "":
                try:
                    if input == "" or 1 <= int(input) <= 30:
                        return True
                except:
                    pass
            return False
        
        # register validation
        vcmd = (exam_options_window.register(validate_entry), '%P')
        number_entry.config(validate="key",
                            validatecommand=vcmd)
        
        # bind arrow clicks
        left_arrow_label.bind("<Button-1>", decrease_number)
        right_arrow_label.bind("<Button-1>", increase_number)
        
        # add visual feedback for arrows
        def on_arrow_enter(event):
            event.widget.config(fg="#9E9E9E")
        
        def on_arrow_leave(event):
            event.widget.config(fg="#FFFFFF")
        
        left_arrow_label.bind("<Enter>", on_arrow_enter)
        left_arrow_label.bind("<Leave>", on_arrow_leave)
        right_arrow_label.bind("<Enter>", on_arrow_enter)
        right_arrow_label.bind("<Leave>", on_arrow_leave)
        
        # confirm button
        def on_confirm():
            selected_count = question_count.get()
            exam_options_window.destroy()
            new_exam(selected_count)
        
        confirm_btn = Util(exam_options_window).button()
        confirm_btn.config(text="Confirm",
                           command=lambda: on_confirm())
        confirm_btn.pack(pady=20)
        
        # set focus to the window and select the number
        number_entry.focus_set()
        number_entry.select_range(0, 'end')
        
        return question_count.get()
    
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
            with open("data/notes.json", "r", encoding="utf-8") as f:
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
            with open("data/notes.json", "w", encoding="utf-8") as f:
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

def new_exam(num_questions=10) -> None:
    """
    Creates a new exam.
    """
    # creates a new window
    new_exam_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - Exam")
    
    # track current question
    current_question = IntVar(value=1)
    
    # exam information frame
    exam_info_frame = Util(new_exam_window).frame()
    exam_info_frame.config(bg="#3A3A3A")
    exam_info_frame.pack(fill="x", padx=10, pady=10)
    
        # question number display
    question_number_frame = Util(exam_info_frame).frame()
    question_number_frame.config(bg="#3A3A3A")
    question_number_frame.pack(side=LEFT)
    
        # current question
    curr_question_label = Util(question_number_frame).label()
    curr_question_label.config(text=f"Q{current_question.get()}",
                               font=("Arial", 24, "bold"),
                               bg="#3A3A3A",
                               fg="white")
    curr_question_label.pack(side=LEFT)
    
        # total number of questions
    total_question_label = Util(question_number_frame).label()
    total_question_label.config(text=f"/ {num_questions}",
                                font=("Arial", 14, "normal"),
                                bg="#3A3A3A",
                                fg="white")
    total_question_label.pack(side=LEFT,
                              pady=(8, 0))
    
        # end exam button
    end_exam_btn = Util(exam_info_frame).button()
    end_exam_btn.config(text="END",
                        font=("Arial", 12, "bold"),
                        bg="#ff4444",
                        fg="white",
                        command=lambda: confirm_end_exam(new_exam_window))
    end_exam_btn.pack(side=RIGHT)
    
    # main content frame (questions and answers)
    content_frame = Util(new_exam_window).frame()
    content_frame.config(bg="#4D4C4C")
    content_frame.pack(fill="both",
                       expand=True,
                       padx=10,
                       pady=(0, 10))
    
        # question frame
    question_frame = Util(content_frame).frame()
    question_frame.config(bg="#4D4C4C")
    question_frame.pack(fill="x", padx=20, pady=20)
    
            # question text
    question_label = Util(question_frame).label()
    question_label.config(font=("Arial", 14, "normal"),
                          bg="#4D4C4C",
                          fg="white",
                          justify=LEFT,
                          wraplength=700)
    question_label.pack(anchor="w")
    
            # multiple choice answers frame
    answers_frame = Util(content_frame).frame()
    answers_frame.config(bg="#4D4C4C")
    answers_frame.pack(fill="both",
                       expand=True,
                       padx=20,
                       pady=20)
    
    # Sample multiple choice answers
    choices = ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"]
    answer_var = StringVar(value="")  # to track selected answer
    
    for choice in choices:
        choice_frame = Util(answers_frame).frame()
        choice_frame.config(bg="#4D4C4C")
        choice_frame.pack(fill="x",
                          pady=5)
        
        # radio button for each choice
        radio_btn = Radiobutton(choice_frame,
                                text=choice,
                                variable=answer_var,
                                value=choice,
                                font=("Arial", 12, "normal"),
                                bg="#4D4C4C",
                                fg="#FFFFFF",
                                selectcolor="#3A3A3A",
                                activebackground="#4D4C4C",
                                activeforeground="white")
        radio_btn.pack(anchor="w")
    
    # navigation frame
    navigation_frame = Util(new_exam_window).frame()
    navigation_frame.config(bg=PROGRAM_BG_COLOR)
    navigation_frame.pack(fill="x",
                          padx=10,
                          pady=10)
    
        # navigation controls
    nav_controls_frame = Util(navigation_frame).frame()
    nav_controls_frame.config(bg=PROGRAM_BG_COLOR)
    nav_controls_frame.pack()
    
            # << label (first question)
    first_label = Util(nav_controls_frame).label()
    first_label.config(text="<<",
                       font=("Arial", 16, "bold"),
                       bg=PROGRAM_BG_COLOR,
                       fg="#FFFFFF",
                       cursor="hand2")
    first_label.pack(side=LEFT, padx=5)
    
            # < label (previous question)
    prev_label = Util(nav_controls_frame).label()
    prev_label.config(text="<",
                      font=("Arial", 16, "bold"),
                      bg=PROGRAM_BG_COLOR,
                      fg="#FFFFFF",
                      cursor="hand2")
    prev_label.pack(side=LEFT,
                    padx=5)
    
            # question number entry
    question_entry = Entry(nav_controls_frame,
                          font=("Arial", 12, "normal"),
                          bg="#4D4C4C",
                          fg="#FFFFFF",
                          width=5,
                          justify="center")
    question_entry.insert(0, str(current_question.get()))
    question_entry.pack(side=LEFT,
                        padx=10)
    
            # > label (next question)
    next_label = Util(nav_controls_frame).label()
    next_label.config(text=">",
                      font=("Arial", 16, "bold"),
                      bg=PROGRAM_BG_COLOR,
                      fg="#FFFFFF",
                      cursor="hand2")
    next_label.pack(side=LEFT,
                    padx=5)
    
            # >> label (last question)
    last_label = Util(nav_controls_frame).label()
    last_label.config(text=">>",
                      font=("Arial", 16, "bold"),
                      bg=PROGRAM_BG_COLOR,
                      fg="#FFFFFF",
                      cursor="hand2")
    last_label.pack(side=LEFT,
                    padx=5)
    
    # navigates to a specific question
    def go_to_question(question_num):
        if 1 <= question_num <= num_questions:
            current_question.set(question_num)
            update_question_display()
    
    # updates the question display
    def update_question_display():
        # update the current question number
        curr_question_label.config(text=f"Q{current_question.get()}")
        
        # update the entry box
        question_entry.delete(0, END)
        question_entry.insert(0, str(current_question.get()))
        
        # update question content
        question_label.config(text="Questions would appear here.")
        
        # update label colors based on availability
        first_label.config(fg="#FFFFFF" if current_question.get() > 1 else "#2A2A2A")
        prev_label.config(fg="#FFFFFF" if current_question.get() > 1 else "#2A2A2A")
        next_label.config(fg="#FFFFFF" if current_question.get() < num_questions else "#2A2A2A")
        last_label.config(fg="#FFFFFF" if current_question.get() < num_questions else "#2A2A2A")
    
    # handles entry box changes
    def on_entry_change(event=None):
        try:
            new_num = int(question_entry.get())
            go_to_question(new_num)
        except ValueError:
            # if invalid input, revert to current question
            question_entry.delete(0, END)
            question_entry.insert(0, str(current_question.get()))
    
    # bind click events to navigation labels
    def on_first_click(event):
        if current_question.get() > 1:
            go_to_question(1)
    
    def on_prev_click(event):
        if current_question.get() > 1:
            go_to_question(current_question.get() - 1)
    
    def on_next_click(event):
        if current_question.get() < num_questions:
            go_to_question(current_question.get() + 1)
    
    def on_last_click(event):
        if current_question.get() < num_questions:
            go_to_question(num_questions)
    
    # bind click events
    first_label.bind("<Button-1>", on_first_click)
    prev_label.bind("<Button-1>", on_prev_click)
    next_label.bind("<Button-1>", on_next_click)
    last_label.bind("<Button-1>", on_last_click)
    
    # add hover effects
    def on_nav_enter(event):
        if event.widget.cget("fg") != "#2A2A2A":  # only change if not disabled
            event.widget.config(fg="#9E9E9E")  # on hover
    
    def on_nav_leave(event):
        # return to appropriate color based on availability
        widget_text = event.widget.cget("text")
        if widget_text == "<<" or widget_text == "<":
            event.widget.config(fg="#FFFFFF" if current_question.get() > 1 else "#2A2A2A")
        else:
            event.widget.config(fg="#FFFFFF" if current_question.get() < num_questions else "#2A2A2A")
    
    # Apply hover effects to all navigation labels
    for nav_label in [first_label, prev_label, next_label, last_label]:
        nav_label.bind("<Enter>", on_nav_enter)
        nav_label.bind("<Leave>", on_nav_leave)
    
    question_entry.bind("<Return>", on_entry_change)
    question_entry.bind("<FocusOut>", on_entry_change)
    
    # confirms ending the exam
    def confirm_end_exam(window):
        from tkinter import messagebox
        
        result = messagebox.askquestion(
            "End Exam",
            "Are you sure you want to end the exam?\n\nThis cannot be undone.",
            icon='warning'
        )
        
        if result == 'yes':
            # You can add exam submission logic here
            messagebox.showinfo("Exam Ended", "Your exam has been submitted.")
            window.destroy()
    
    # initialize the display
    update_question_display()

def view_notes() -> None:
    """
    View all current notes.
    """
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
        with open("data/notes.json", "r", encoding="utf-8") as f:
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
                with open("data/notes.json", "r", encoding="utf-8") as f:
                    notes_data = json.load(f)
                
                # remove the note
                if note_id in notes_data:
                    del notes_data[note_id]
                    
                    # save updated data
                    with open("data/notes.json", "w", encoding="utf-8") as f:
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
            
def view_exams() -> None:
    """
    View all past exams.
    """
    pass

if __name__ == "__main__":
    main_window = Window()
    menu()
    main_window.run()