from tkinter import  Tk
from work.frames.taskFrame import TaskFrame
from work.frames.previewFrame import PreviewFrame
from work.frames.arrowFrame import ArrowFrame
from work.frames.toolsFrame import ToolsFrame

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("test")
        self.geometry("800x560+100+100")
        self.resizable(False, False)  # 윈도우 크기 고정
        ###################### define frame ######################
        tools_frame = ToolsFrame(self)
        tools_frame.pack(side="bottom", expand=True, fill="both")

        self.task_frame = TaskFrame(self,main=self)
        self.task_frame.pack(side="left", expand=True, fill="both")
        self.task_frame.pack_propagate(False) # 크기고정

        arrow_frame = ArrowFrame(self)
        arrow_frame.pack(side="left", fill="both")

        self.preview_frame = PreviewFrame(self)
        self.preview_frame.pack(side="left", expand=True, fill="both")
        self.preview_frame.pack_propagate(False) # 크기고정
        ####################### end_define frame #################

    def update_task_view(self,img):
        img_width = img.width()
        img_height = img.height()
        self.task_frame.task_canvas.config(width=img_width, height=img_height)
        self.task_frame.task_canvas.create_image( img_width/2, img_height/2, image=img)
        self.task_frame.task_canvas.image_names=img

    def update_preview(self, img):
        img_width = img.width()
        img_height = img.height()
        self.preview_frame.pre_canvas.config(width=img_width, height=img_height)
        self.preview_frame.pre_canvas.create_image(img_width/2, img_height/2, image=img)
        self.preview_frame.pre_canvas.image_names = img

    #중복되는 파라미터 관리 필요. 너무 많아짐

main = MainWindow()
main.mainloop()

