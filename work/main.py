from tkinter import  Tk,filedialog,Label,PhotoImage,Frame,Button
import numpy as np, cv2
from PIL import Image,ImageTk
from utils.file import openfile

class MainWindow(Tk):

    def __init__(self):
        super().__init__()
        self.title("test")

        self.geometry("1200x800+100+100")
       # self.resizable(False, False)  # 윈도우 크기 고정

        self.left_frame = Frame(self, bg="lightblue", width=100, height=400)
        self.left_frame.pack(side="left", expand=True, fill="both")

        center_frame = Frame(self, width=200, height=400)
        center_frame.pack(side="left", fill="both")

        right_frame = Frame(self, bg="lightcoral", width=100, height=400)
        right_frame.pack(side="left", expand=True, fill="both")

        open_button = Button(self.left_frame, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=20)

        arr_button = Button(center_frame, text="->", state="disabled")  # 비활성화
        arr_button.pack(pady=20, side="right")

        download_button = Button(right_frame, text="download")
        download_button.pack(pady=20)

    def on_click_open_button(self):# 클릭 콜백 함수 선택한 이미지를 왼쪽 프레임에 표시함.
        image = openfile()
        label = Label(self.left_frame, image=image)
        label.image = image
        label.pack()


main = MainWindow()
main.mainloop()

