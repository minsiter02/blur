from tkinter import Label,Frame,Button,Canvas
from work.utils.image_process import ImageProcess
class TaskFrame(Frame):
    def __init__(self, parent,main):
        super().__init__(parent, bg="lightblue", height=500)
        self.main = main
        self.img_process = ImageProcess()

        open_button = Button(self, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=5)

        self.task_canvas = Canvas(self,width=0,height=0)
        self.task_canvas.pack()


    def on_click_open_button(self):  # 클릭 함수 이미지를 교체 함.
        image = self.img_process.openfile()
        # main 을 거쳐 각 frame 이미지를 업데이트
        self.main.update_task_view(image)
        self.main.update_preview(image)
