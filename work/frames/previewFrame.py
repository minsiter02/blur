from tkinter import Frame,Button,Canvas
from work.frames.ImageSettingsWindow import ImageSettingsWindow

class PreviewFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, height=500,background="light gray")
        download_button = Button(self, text="download", command=self.on_click_download_button)
        download_button.pack(pady=5)

        self.pre_canvas = Canvas(self, width=0, height=0,highlightthickness=0)
        self.pre_canvas.place(relx=0.5, rely=0.52, anchor="center")

    def on_click_download_button(self):
        ImageSettingsWindow(self)