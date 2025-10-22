from tkinter import *

PROGRAM_BG_COLOR = "#3A3A3A"
BUTTON_BG_COLOR = "#FFFFFF"

class Util:
    def __init__(self, window):
        self._window = window
    
    def label(self):
        return Label(self._window,
                     bg=PROGRAM_BG_COLOR,
                     fg=BUTTON_BG_COLOR)
    
    def button(self):
        return Button(self._window,
                      bg=BUTTON_BG_COLOR,
                      relief=FLAT,
                      padx=15,
                      pady=5,
                      cursor="hand2",
                      font=("Arial", 24, "normal"))
        
    def frame(self):
        return Frame(self._window,
                     bg=PROGRAM_BG_COLOR)