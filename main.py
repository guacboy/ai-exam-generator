from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk
import PIL.Image as PImage
import json
import os
from datetime import datetime
import subprocess
import threading
import os

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
    
    # feedback button framework
    feedback_framework = Util(main_window.get_window()).frame()
    feedback_framework.pack(side=BOTTOM, pady=(0, 50))
    
        # feedback button
    feedback_btn = Util(feedback_framework).button()
    feedback_btn.config(text="Submit Feedback",
                       command=lambda: submit_feedback(),
                       font=("Arial", 14, "normal"))
    feedback_btn.pack()
        # tooltip
    feedback_tooltip = ToolTip(feedback_btn, "Share your feedback to help improve ExamAI.")
    
    # view button framework
    view_framework = Util(main_window.get_window()).frame()
    view_framework.pack(side=BOTTOM,
                        pady=(0, 100))
    
        # view notes button
    view_notes_btn = Util(view_framework).button()
    view_notes_btn.config(text="View Notes",
                          command=lambda: view_notes())
    view_notes_btn.pack(side=LEFT)
        # tooltip
    view_notes_tooltip = ToolTip(view_notes_btn, "View previous notes.")
    
        # view exams button
    view_exams_btn = Util(view_framework).button()
    view_exams_btn.config(text="View Exams",
                          command=lambda: view_exams())
    view_exams_btn.pack(side=LEFT,
                        padx=(25, 0))
        # tooltip
    view_exams_tooltip = ToolTip(view_exams_btn, "View previous exams.")
    
    # new note button
    new_note_btn = Util(main_window.get_window()).button()
    new_note_btn.config(text="New Note",
                        command=lambda: new_note())
    new_note_btn.pack(side=BOTTOM,
                      pady=(0, 25))
        # tooltip
    new_note_tooltip = ToolTip(new_note_btn, "Create a new note.")

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

def new_exam(num_questions=10,
             graded_mode=False,
             user_answers=None,
             correct_answers=None) -> None:
    """
    Creates a new exam.
    """
    # creates a new window
    if graded_mode:
        new_exam_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - Exam Results")
    else:
        new_exam_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - Exam")
    
    # track current question and user answers
    current_question = IntVar(value=1)
    
    # if this is a graded view, use provided answers;
    # otherwise initialize empty
    if graded_mode and user_answers is not None:
        exam_user_answers = user_answers
        exam_graded = True
    else:
        exam_user_answers = {}
        exam_graded = False
    
    # default correct answers (replace this with AI-generated answers)
    if correct_answers is None:
        correct_answers = {
            1: "A) First option",
            2: "B) Second option", 
            3: "C) Third option",
            4: "D) Fourth option",
        }
    
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
    
    # feedback buttons frame (visible only in graded mode)
    feedback_frame = Util(exam_info_frame).frame()
    feedback_frame.config(bg="#3A3A3A")
    feedback_frame.pack(side=RIGHT)
    
        # thumbs down button
    thumbs_down_icon = None
    thumbs_down_btn = Util(feedback_frame).button()
    
        # thumbs up button  
    thumbs_up_icon = None
    thumbs_up_btn = Util(feedback_frame).button()
    
        # load feedback icons (only in graded mode)
    if graded_mode:
        try:
            # thumbs down
            pil_image = PImage.open("./assets/thumbs_down_icon.png")
            pil_image = pil_image.resize((32, 32))
            thumbs_down_icon = ImageTk.PhotoImage(pil_image)
            thumbs_down_btn.config(image=thumbs_down_icon, 
                                bg="#3A3A3A",
                                relief="flat",
                                command=lambda: save_feedback("negative"))
            thumbs_down_btn.image = thumbs_down_icon
            
            # thumbs up
            pil_image = PImage.open("./assets/thumbs_up_icon.png")
            pil_image = pil_image.resize((32, 32))
            thumbs_up_icon = ImageTk.PhotoImage(pil_image)
            thumbs_up_btn.config(image=thumbs_up_icon,
                                bg="#3A3A3A", 
                                relief="flat",
                                command=lambda: save_feedback("positive"))
            thumbs_up_btn.image = thumbs_up_icon
            
            thumbs_down_btn.pack(side=LEFT, padx=5)
            thumbs_up_btn.pack(side=LEFT, padx=5)
            
            # tooltips
            thumbs_up_tooltip = ToolTip(thumbs_up_btn, "See more questions\nlike this.")
            thumbs_down_tooltip = ToolTip(thumbs_down_btn, "See less questions\nlike this.")
            
            feedback_frame.pack(side=RIGHT)
            
        except Exception as e:
            print(f"Could not load feedback icons: {e}")
    
        # end exam button (only in non-graded mode)
    end_exam_btn = Util(exam_info_frame).button()
    if not graded_mode:
        end_exam_btn.config(text="END",
                            font=("Arial", 12, "bold"),
                            bg="#ff4444",
                            fg="white",
                            command=lambda: confirm_end_exam(new_exam_window, exam_user_answers, correct_answers))
        end_exam_btn.pack(side=RIGHT)
    else:
        # in graded mode, don't show the end exam button
        end_exam_btn.pack_forget()
    
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
    
    # sample multiple choice answers
    choices = ["A) First option", "B) Second option", "C) Third option", "D) Fourth option"]
    answer_var = StringVar(value="")  # to track selected answer
    
    # store radio buttons for later highlighting
    radio_buttons = []
    
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
        radio_buttons.append(radio_btn)
        
    # save user's answer (only in non-graded mode)
    def save_answer():
        if not graded_mode:
            user_answers[current_question.get()] = answer_var.get()
    
    # update radio button when answer changes (only in non-graded mode)
    if not graded_mode:
        answer_var.trace('w', lambda *args: save_answer())
    
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
        
        # load user's answer for this question if exists
        if current_question.get() in user_answers:
            answer_var.set(user_answers[current_question.get()])
        else:
            answer_var.set("")  # clear if no answer
        
        # highlight answers if exam is graded
        if exam_graded:
            highlight_answers()
        
        # update label colors based on availability
        first_label.config(fg="#FFFFFF" if current_question.get() > 1 else "#2A2A2A")
        prev_label.config(fg="#FFFFFF" if current_question.get() > 1 else "#2A2A2A")
        next_label.config(fg="#FFFFFF" if current_question.get() < num_questions else "#2A2A2A")
        last_label.config(fg="#FFFFFF" if current_question.get() < num_questions else "#2A2A2A")
        
    # Function to highlight correct/incorrect answers
    def highlight_answers():
        current_q = current_question.get()
        if current_q in correct_answers:
            correct_answer = correct_answers[current_q]
            user_answer = user_answers.get(current_q, "")
            
            for radio in radio_buttons:
                choice_text = radio.cget("text")
                if choice_text == correct_answer:
                    # Highlight correct answer in green
                    radio.config(bg="#73FF73", fg="black")
                elif choice_text == user_answer and user_answer != correct_answer:
                    # Highlight incorrect user answer in red
                    radio.config(bg="#FF3030", fg="black")
                else:
                    # Reset other options
                    radio.config(bg="#4D4C4C", fg="#FFFFFF")
    
    # grades the exam
    def grade_exam(user_answers_dict, correct_answers_dict):
        score = 0
        for q_num in range(1, num_questions + 1):
            if q_num in user_answers_dict and q_num in correct_answers_dict:
                if user_answers_dict[q_num] == correct_answers_dict[q_num]:
                    score += 1
        
        return score
    
    # saves exam data
    def save_exam_data(score, user_answers_dict, correct_answers_dict):
        # create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        exam_data = {
            "timestamp": datetime.now().isoformat(),
            "num_questions": num_questions,
            "score": score,
            "user_answers": user_answers,
            "correct_answers": correct_answers
        }
        
        try:
            # load existing exams if file exists
            if os.path.exists("data/exam.json"):
                with open("data/exam.json", "r") as f:
                    all_exams = json.load(f)
            else:
                all_exams = []
            
            # add new exam data
            all_exams.append(exam_data)
            
            # save back to file
            with open("data/exam.json", "w") as f:
                json.dump(all_exams, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving exam data: {e}")
            return False
    
    # saves user feedback
    def save_feedback(feedback_type):
        # load existing exams
        try:
            if os.path.exists("data/exam.json"):
                with open("data/exam.json", "r") as f:
                    all_exams = json.load(f)
                
                # add feedback to the most recent exam
                if all_exams:
                    all_exams[-1]["feedback"] = feedback_type
                    
                    # save back
                    with open("data/exam.json", "w") as f:
                        json.dump(all_exams, f, indent=2)
            else:
                messagebox.showwarning("Error", "No exam data found to add feedback to.")
        except Exception as e:
            print(f"Error saving feedback: {e}")
    
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
    def confirm_end_exam(window, user_answers_dict, correct_answers_dict):
        result = messagebox.askquestion(
            "End Exam",
            "Are you sure you want to end the exam?\n\nThis cannot be undone.",
            icon='warning'
        )
        
        if result == "yes":
            # grade the exam
            score = grade_exam(user_answers_dict, correct_answers_dict)
            
            # save exam data
            save_exam_data(score, user_answers_dict, correct_answers_dict)
            
            # close the current exam window
            window.destroy()
            
            # reopen in graded mode with the same questions and user answers
            new_exam(num_questions=num_questions, 
                     graded_mode=True, 
                     user_answers=user_answers_dict, 
                     correct_answers=correct_answers_dict)
    
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
    view_exams_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - View Exams")
    
    # search exams frame
    search_exams_frame = Util(view_exams_window).frame()
    search_exams_frame.pack(side=TOP,
                            pady=(0, 5))
    
    # load and resize image
    pil_image = PImage.open("./assets/search_icon.png")
    pil_image = pil_image.resize((32, 32))  # resize
    search_icon = ImageTk.PhotoImage(pil_image)
    # search image
    search_label = Util(search_exams_frame).label()
    search_label.config(image=search_icon)
    search_label.image = search_icon  # keeps reference
    search_label.pack(side=LEFT)
    
    # search exams text
    search_exams_text = Util(search_exams_frame).text()
    search_exams_text.config(font=("Arial", 16, "normal"),
                             bg="#4D4C4C",
                             height=1)
    search_exams_text.pack(side=LEFT)
    
    # add placeholder
    placeholder_text = "Search..."
    search_exams_text.insert("1.0", placeholder_text)
    search_exams_text.config(fg="gray")

    def clear_placeholder(event):
        if search_exams_text.get("1.0", "end-1c") == placeholder_text:
            search_exams_text.delete("1.0", "end")
            search_exams_text.config(fg="white")

    def add_placeholder_if_empty(event):
        if not search_exams_text.get("1.0", "end-1c").strip():
            search_exams_text.insert("1.0", placeholder_text)
            search_exams_text.config(fg="gray")

    search_exams_text.bind("<FocusIn>", clear_placeholder)
    search_exams_text.bind("<FocusOut>", add_placeholder_if_empty)
    
    # load exams data
    try:
        with open("data/exam.json", "r", encoding="utf-8") as f:
            exams_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        exams_data = []
        
    # exams list frame
    exams_frame = Util(view_exams_window).frame()
    exams_frame.pack(side=LEFT,
                     anchor=NW,
                     fill="x",
                     expand=True,
                     padx=10,
                     pady=(0, 5))
    
    if not exams_data:
        # no exams message
        no_exams_label = Util(exams_frame).label()
        no_exams_label.config(text="No exams found. Generate an exam to get started!",
                             font=("Arial", 12, "normal"))
        no_exams_label.pack(pady=50)
    else:
        # display each exam (reverse to show most recent first)
        for exam_index, exam_data in enumerate(reversed(exams_data)):
            # exam container frame for the entire exam row
            exam_container = Util(exams_frame).frame()
            exam_container.pack(fill="x",
                                pady=5)
            
            # individual exam frame
            exam_frame = Util(exam_container).frame()
            exam_frame.config(bg="#4D4C4C")
            exam_frame.pack(side=LEFT,
                            fill="x",
                            expand=True)
            
            # exam date and score
            timestamp = exam_data.get("timestamp", "")
            if timestamp:
                try:
                    exam_date = datetime.fromisoformat(timestamp)
                    formatted_date = exam_date.strftime("%m/%d/%Y %H:%M")
                except ValueError:
                    formatted_date = "Unknown"
            else:
                formatted_date = "Unknown"
            
            score = exam_data.get("score", 0)
            num_questions = exam_data.get("num_questions", 0)
            percentage = exam_data.get("percentage", 0)
            
            # exam title label (date and score)
            exam_title_label = Util(exam_frame).label()
            exam_title_label.config(text=f"Exam - {formatted_date}",
                                    font=("Arial", 12, "bold"),
                                    bg="#4D4C4C")
            exam_title_label.pack(anchor=W)

            # exam score label
            exam_score_label = Util(exam_frame).label()
            exam_score_label.config(text=f"Score: {score}/{num_questions} ({percentage:.1f}%)",
                                    font=("Arial", 12, "normal"),
                                    bg="#4D4C4C")
            exam_score_label.pack(anchor=W)
            
            # separate frame for buttons on the right
            button_frame = Util(exam_container).frame()
            button_frame.pack(side=RIGHT,
                              padx=(10, 0))
            
            # load and resize image for edit button
            pil_image = PImage.open("./assets/edit_icon.png")
            pil_image = pil_image.resize((42, 42))  # resize
            edit_icon = ImageTk.PhotoImage(pil_image)
            # edit button
            edit_btn = Util(button_frame).button()
            edit_btn.config(image=edit_icon,
                              command=lambda idx=len(exams_data)-1-exam_index: open_exam(idx))
            edit_btn.image = edit_icon  # keeps reference
            edit_btn.pack(side=LEFT,
                            padx=(0, 10))
            
            # load and resize image for delete button
            pil_image = PImage.open("./assets/delete_icon.png")
            pil_image = pil_image.resize((42, 42))  # resize
            delete_icon = ImageTk.PhotoImage(pil_image)
            # delete button
            delete_btn = Util(button_frame).button()
            delete_btn.config(image=delete_icon,
                              command=lambda idx=len(exams_data)-1-exam_index, dt=formatted_date: confirm_delete_exam(idx, dt))
            delete_btn.image = delete_icon  # keeps reference
            delete_btn.pack(side=LEFT)
            
    def confirm_delete_exam(exam_index, exam_date):
        """
        Show confirmation dialog before deleting an exam.
        """
        response = messagebox.askquestion(
            "Confirm Delete",
            f"Are you sure you want to delete\nexam from {exam_date}?\n\nThis cannot be undone.",
            icon='warning',
        )
        
        if response == 'yes':
            delete_exam(exam_index)

    def delete_exam(exam_index):
        """
        Actually delete the exam from the JSON file and refresh the view.
        """
        try:
            # load current exams data
            with open("data/exam.json", "r", encoding="utf-8") as f:
                exams_data = json.load(f)
            
            # remove the exam
            if 0 <= exam_index < len(exams_data):
                del exams_data[exam_index]
                
                # save updated data
                with open("data/exam.json", "w", encoding="utf-8") as f:
                    json.dump(exams_data, f, indent=2, ensure_ascii=False)
                
                # show success message
                messagebox.showinfo("Success", "Exam deleted successfully.")
                
                # refresh the view exams window
                refresh_exams_view()
            else:
                messagebox.showerror("Error", "Exam not found.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete exam: {str(e)}")

    def refresh_exams_view():
        """
        Refresh the view exams window to reflect changes.
        """
        # close the current view exams window
        view_exams_window.destroy()
        # reopen the view exams window
        view_exams()
        
    def open_exam(exam_index):
        """
        Open an existing exam in review mode.
        """
        try:
            # load exams data
            with open("data/exam.json", "r", encoding="utf-8") as f:
                exams_data = json.load(f)
            
            if 0 <= exam_index < len(exams_data):
                exam_data = exams_data[exam_index]
                
                # close the view exams window
                view_exams_window.destroy()
                
                # open the exam in graded mode
                new_exam(
                    num_questions=exam_data.get("num_questions", 10),
                    graded_mode=True,
                    user_answers=exam_data.get("user_answers", {}),
                    correct_answers=exam_data.get("correct_answers", {})
                )
            else:
                messagebox.showerror("Error", "Exam not found.")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open exam: {str(e)}")
            
def submit_feedback() -> None:
    """
    Window to submit feedback about the application.
    """
    feedback_window = main_window.create_toplevel(f"{PROGRAM_TITLE} - Submit Feedback", "600x500")
    
    # title
    title_label = Util(feedback_window).label()
    title_label.config(text="We'd Love Your Feedback!",
                       font=("Arial", 20, "bold"))
    title_label.pack(pady=(20, 10))
    
    # description
    desc_label = Util(feedback_window).label()
    desc_label.config(text="Your feedback helps us improve ExamAI.",
                      font=("Arial", 12, "normal"))
    desc_label.pack(pady=(0, 20))
    
    # feedback text area with scrollbar
    text_frame = Util(feedback_window).frame()
    text_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))
    
    feedback_text = Text(text_frame,
                        bg="#1E1E1E",
                        fg="white",
                        font=("Arial", 12, "normal"),
                        wrap=WORD,
                        height=15)
    
    scrollbar = Scrollbar(text_frame, orient=VERTICAL, command=feedback_text.yview)
    feedback_text.configure(yscrollcommand=scrollbar.set)
    
    feedback_text.pack(side=LEFT, fill=BOTH, expand=True)
    scrollbar.pack(side=RIGHT, fill=Y)
    
    # add placeholder
    placeholder_text = "Please share your thoughts, suggestions, or report any issues you've encountered..."
    feedback_text.insert("1.0", placeholder_text)
    feedback_text.config(fg="gray")

    def clear_placeholder(event):
        if feedback_text.get("1.0", "end-1c") == placeholder_text:
            feedback_text.delete("1.0", "end")
            feedback_text.config(fg="white")

    def add_placeholder_if_empty(event):
        if not feedback_text.get("1.0", "end-1c").strip():
            feedback_text.insert("1.0", placeholder_text)
            feedback_text.config(fg="gray")

    feedback_text.bind("<FocusIn>", clear_placeholder)
    feedback_text.bind("<FocusOut>", add_placeholder_if_empty)
    
    # status label
    status_label = Util(feedback_window).label()
    status_label.config(text="", font=("Arial", 10, "normal"))
    status_label.pack(pady=(0, 10))
    
    # button frame
    button_frame = Util(feedback_window).frame()
    button_frame.pack(side=BOTTOM, pady=(0, 20))
    
    def submit_feedback_action():
        """Submit feedback by writing to the JSON file in microservice folder."""
        feedback_content = feedback_text.get("1.0", "end-1c").strip()
        
        if not feedback_content or feedback_content == placeholder_text:
            status_label.config(text="Please enter some feedback before submitting.", fg="red")
            return
            
        # disable submit button during submission
        submit_btn.config(state=DISABLED)
        cancel_btn.config(state=DISABLED)
        status_label.config(text="Submitting your feedback...", fg="white")
        
        try:
            # write feedback to json file
            success = write_feedback_to_json(feedback_content)
            
            if success:
                status_label.config(text="✓ Thank you for your feedback! It has been submitted.", fg="green")
                # show success for 3 seconds then close
                feedback_window.after(3000, feedback_window.destroy)
            else:
                status_label.config(text="✗ Failed to submit feedback. Please try again.", fg="red")
                # re-enable buttons on error
                submit_btn.config(state=NORMAL)
                cancel_btn.config(state=NORMAL)
                
        except Exception as e:
            status_label.config(text=f"✗ Error: {str(e)}", fg="red")
            submit_btn.config(state=NORMAL)
            cancel_btn.config(state=NORMAL)
    
    def write_feedback_to_json(feedback_content):
        """Write feedback to a JSON file in the microservice folder."""
        try:
            # microservice is in a subfolder
            microservice_folder = "feedback-analyzer-microservice"
            
            # create the folder if it doesn't exist
            os.makedirs(microservice_folder, exist_ok=True)
            
            # json file path
            json_filepath = os.path.join(microservice_folder, "feedbacks.json")
            
            # prepare feedback data
            feedback_data = {
                'timestamp': datetime.now().isoformat(),
                'feedback': feedback_content,
                'status': 'pending'  # mark as pending analysis
            }
            
            # read existing feedbacks or create new list
            if os.path.exists(json_filepath):
                try:
                    with open(json_filepath, 'r', encoding='utf-8') as f:
                        all_feedbacks = json.load(f)
                except:
                    all_feedbacks = []
            else:
                all_feedbacks = []
            
            # add new feedback
            all_feedbacks.append(feedback_data)
            
            # write back to file
            with open(json_filepath, 'w', encoding='utf-8') as f:
                json.dump(all_feedbacks, f, indent=2, ensure_ascii=False)
            
            print(f"feedback added to: {json_filepath}")
            return True
            
        except Exception as e:
            print(f"error writing feedback json: {e}")
            return False
    
    # submit button
    submit_btn = Util(button_frame).button()
    submit_btn.config(text="✓ Submit Feedback",
                      font=("Arial", 14, "bold"),
                      bg="#4CAF50",
                      fg="white",
                      padx=20,
                      pady=10,
                      command=submit_feedback_action)
    submit_btn.pack(side=LEFT, padx=(0, 10))
    
    # cancel button
    cancel_btn = Util(button_frame).button()
    cancel_btn.config(text="Cancel",
                      font=("Arial", 14, "normal"),
                      command=feedback_window.destroy)
    cancel_btn.pack(side=LEFT)
            
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.id = None
        widget.bind("<Enter>", self.schedule_tooltip)
        widget.bind("<Leave>", self.hide_tooltip)
        widget.bind("<ButtonPress>", self.hide_tooltip)
    
    def schedule_tooltip(self, event=None):
        self.id = self.widget.after(500, self.show_tooltip)  # Show after 500ms delay
    
    def show_tooltip(self):
        x = self.widget.winfo_rootx() + self.widget.winfo_width() + 5
        y = self.widget.winfo_rooty() + (self.widget.winfo_height() // 2)
        
        self.tooltip = Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        
        label = Label(self.tooltip, 
                     text=self.text, 
                     justify=LEFT,
                     background="#1E1E1E",
                     foreground="#FFFFFF",
                     relief="flat", 
                     borderwidth=0,
                     font=("Arial", 9, "normal"),
                     padx=8, 
                     pady=4)
        label.pack()
        
        # add a small arrow pointer
        arrow = Frame(self.tooltip, 
                     background="#FFFFFF", 
                     width=8, 
                     height=8)
        arrow.place(x=-4, y=10)  # position arrow to the left
    
    def hide_tooltip(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
            
if __name__ == "__main__":
    main_window = Window()
    menu()
    main_window.run()