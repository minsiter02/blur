from tkinter import  Tk
from work.frames.taskFrame import TaskFrame
from work.frames.previewFrame import PreviewFrame
from work.frames.arrowFrame import ArrowFrame
from work.frames.toolsFrame import ToolsFrame

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("test")
        self.geometry("800x600+100+100")
        #self.resizable(False, False)  # 윈도우 크기 고정
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

    def update_preview_frame(self,img):
        self.preview_frame.task_label.image = img
        self.preview_frame.task_label.config(image=img)
main = MainWindow()
main.mainloop()

