from tkinter import Frame,Canvas,ttk
from frames.ImageSettingsWindow import ImageSettingsWindow
from utils.image_process import ImageProcess

class PreviewFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, height=500)
        self.download_button = ttk.Button(self, text="download", command=self.on_click_download_button)
        self.download_button.pack(pady=5)

        self.canvas_frame = Frame(self)
        self.canvas_frame.place(relx=0.5, rely=0.54, anchor="center")
        self.pre_canvas = Canvas(self.canvas_frame, width=0, height=0, highlightthickness=0)
        self.pre_canvas.pack()

    def on_click_download_button(self):
        if ImageProcess.image is None: return
        ImageSettingsWindow(self)