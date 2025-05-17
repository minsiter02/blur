from tkinter import Frame,Button,Scale
class ToolsFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="blue",height=100)
        button = Button(self, text="gggggg")
        button.pack(side="right")
        button2 = Button(self, text="dddd")
        button2.pack(side="right")
        scale = Scale(self, variable=1.0, command=self.select, orient="horizontal", showvalue=False)
        scale.pack()

    def select(self, event):
        print(event)