from tkinter import  Tk,Label,Frame,Button,Scale

import utils.file as File

from work.frames.ImageSettingsWindow import ImageSettingsWindow

## 클래스로 나누기
class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("test")

        self.geometry("800x600+100+100")
        #self.resizable(False, False)  # 윈도우 크기 고정

        ###################### define frame ######################
        top_frame = Frame(self,bg="green",height=500)
        top_frame.pack(side="top",expand=True,fill="both")

        bottom_frame = Frame(self, bg="blue",height=100)
        bottom_frame.pack(side="bottom", expand=True,fill="both")

        self.left_frame = Frame(top_frame, bg="lightblue",  height=500)
        self.left_frame.pack(side="left", expand=True, fill="both")
        self.left_frame.pack_propagate(False) # 크기고정

        center_frame = Frame(top_frame,bg= "green")
        center_frame.pack(side="left", fill="both")

        right_frame = Frame(top_frame, bg="lightcoral",  height=500)
        right_frame.pack(side="left", expand=True, fill="both")
        right_frame.pack_propagate(False) # 크기고정
        ####################### end_define frame #################

    ########################### top_frame ############################
        ####################### left_frame #######################
        open_button = Button(self.left_frame, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=20)

        self.task_label = Label(self.left_frame)
        self.task_label.pack()
        ###################### end_left_frame ####################

        ###################### center_frame ######################
        arr_button = Button(center_frame, text="->", state="disabled")  # 비활성화
        arr_button.pack(side="right")
        ###################### end_center_frame ##################

        ###################### right_frame #######################
        download_button = Button(right_frame, text="download", command=self.on_click_download_button)
        download_button.pack(pady=20)
        ###################### end_right_frame ###################
    ########################## end_top_frame #########################

    ########################## bottom_frame_frame ########################
        button = Button(bottom_frame,text="gggggg")
        button.pack(side="right")
        button2 = Button(bottom_frame,text="dddd")
        button2.pack(side="right")
        scale = Scale(bottom_frame, variable=1.0, command=self.select, orient="horizontal", showvalue=False)
        scale.pack()
    ########################## end_bottom_frame_frame ####################

    def on_click_open_button(self):# 클릭 콜백 함수 이미지를 교체 함.
        image = File.openfile()
        self.task_label.image = image
        self.task_label.config(image=image)
    def on_click_download_button(self):
        ImageSettingsWindow(self)


    def select(self,event):
        print(event)

main = MainWindow()
main.mainloop()

