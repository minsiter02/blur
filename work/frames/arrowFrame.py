from tkinter import Frame
from tkinter.ttk import Button
class ArrowFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        arr_button = Button(self, text="->", state="disabled",width=3)  # 비활성화
        arr_button.pack(side="right")
