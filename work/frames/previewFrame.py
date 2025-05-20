from tkinter import Label,Frame,Button,Canvas
from work.utils.image_process import ImageProcess
from work.frames.ImageSettingsWindow import ImageSettingsWindow
class PreviewFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightcoral", height=500)
        download_button = Button(self, text="download", command=self.on_click_download_button)
        download_button.pack(pady=5)

        self.img_process = ImageProcess()

        self.pre_canvas = Canvas(self, width=0, height=0)
        self.pre_canvas.pack()

    def on_click_download_button(self):
        ImageSettingsWindow(self)