import random
from tkinter import Frame,Button,Canvas
from work.utils.file import openfile
from work.utils.color import rgb_to_hex
class TaskFrame(Frame):
    def __init__(self, parent,main):
        super().__init__(parent, bg="lightblue", height=500)
        self.main = main

        open_button = Button(self, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=5)

        self.task_canvas = Canvas(self,width=0,height=0)
        self.task_canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.task_canvas.bind("<ButtonPress-1>", self.on_press)
        self.task_canvas.bind("<B1-Motion>", self.on_drag)
        self.task_canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click_open_button(self):  # 클릭 함수 이미지를 교체 함.
        image = openfile()
        # main 을 거쳐 각 frame 이미지를 업데이트
        self.main.update_task_view(image)
        self.main.update_preview(image)

    def on_press(self, event): #마우스를 처음 누룰 때 시작 좌표 설정
        self.start_x = event.x
        self.start_y = event.y
        #self.rect는 사각형 식별자임.
        rgb = [random.randint(0, 255) for _ in range(3)] # 지금은 랜덤이지만 세기, 모양에 따라 달라지도록 구현
        self.rect = self.task_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, fill=rgb_to_hex(rgb) ,outline="blue", width=2)

    def on_drag(self, event): # 드래그 중일 때 
        self.task_canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event): # 드래그 완료 후 사각형 확정
        self.task_canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)



