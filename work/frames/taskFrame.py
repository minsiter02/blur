import random
from tkinter import Frame,Button,Canvas
from work.utils.file import open_image, return_resize_tkimg
from work.utils.color import rgb_to_hex
from work.utils.image_process import blur

class TaskFrame(Frame):
    def __init__(self, parent,main):
        super().__init__(parent, bg="lightblue", height=500)
        self.main = main

        open_button = Button(self, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=5)

        self.task_canvas = Canvas(self,width=0,height=0,highlightthickness=0)
        self.task_canvas.place(relx=0.5, rely=0.5, anchor="center")

        self.start_x = None
        self.start_y = None
        self.blur_config = [] #[ [id,type],[id,type],...,[id,type] ]
        self.task_canvas.bind("<ButtonPress-1>", self.on_press)
        self.task_canvas.bind("<B1-Motion>", self.on_drag)
        self.task_canvas.bind("<ButtonRelease-1>", self.on_release)
        self.task_canvas.bind("<Button-3>",self.delete)

    def on_click_open_button(self):  # 클릭 함수 이미지를 교체 함.
        image = open_image()
        if image is None:
            pass
        else:
            # main 을 거쳐 각 frame 이미지를 업데이트
            tk_image = return_resize_tkimg(image)
            self.main.update_task_view(tk_image)
            self.main.update_preview(tk_image)

    def delete(self,event): # 임시 undo 함수.
        self.task_canvas.delete(self.blur_config[-1][0])
        self.blur_config.pop()

    def on_press(self, event): #마우스를 처음 누룰 때 시작 좌표 설정
        self.start_x = event.x
        self.start_y = event.y
        #self.blur_history_keys 는 도형의 식별자임.
        rgb = [random.randint(0, 255) for _ in range(3)] # 지금은 랜덤이지만 세기, 모양에 따라 달라지도록 구현
        key = []
        if rgb[0] > 120:
            key.append(self.task_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, fill=rgb_to_hex(rgb), outline="blue", width=2))
            key.append("rect")
        else:
            key.append(self.task_canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, fill=rgb_to_hex(rgb), outline="red", width=2))
            key.append("circle")
        self.blur_config.append(key)

    def on_drag(self, event): # 드래그 중일 때
        self.task_canvas.coords(self.blur_config[-1][0], self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event): # 드래그 완료 후 도형 확정
        if self.start_x == event.x or self.start_y == event.y: # 바로 놓을 경우 삭제함.
            self.task_canvas.delete(self.blur_config[-1][0])
            self.blur_config.pop()
        else:
            self.task_canvas.coords(self.blur_config[-1][0], self.start_x, self.start_y, event.x, event.y)
            coords = [self.start_x,self.start_y,event.x,event.y]
            ### 다른 방향으로 드래그시 좌표 스와핑
            if self.start_x > event.x:
                coords[0], coords[2] = coords[2], coords[0]
            if self.start_y > event.y:
                coords[1], coords[3] = coords[3], coords[1]

            image = blur(coords= coords, blur_config = self.blur_config[-1]) #블러 함수 호출
            preview_img = return_resize_tkimg(image) # 리사이즈 된 Canvas 전용 이미지
            self.main.update_preview(preview_img) #
            print(self.blur_config)
            print(self.start_x, self.start_y)