from tkinter import Label,Frame,Button
from work.utils.image_process import ImageProcess
from work.frames.ImageSettingsWindow import ImageSettingsWindow
class PreviewFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightcoral", height=500)
        download_button = Button(self, text="download", command=self.on_click_download_button)
        download_button.pack(pady=20)

        self.img_process = ImageProcess()

        self.task_label = Label(self)
        self.task_label.pack()

    def on_click_download_button(self):
        ImageSettingsWindow(self)