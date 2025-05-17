from tkinter import Label,Frame,Button
from work.utils.image_process import ImageProcess
class TaskFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightblue", height=500)

        self.img_process = ImageProcess()

        open_button = Button(self, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=20)

        self.task_label = Label(self)
        self.task_label.pack()

    def on_click_open_button(self):  # 클릭 함수 이미지를 교체 함.
        image = self.img_process.openfile()
        self.task_label.image =  image
        self.task_label.config(image=image)