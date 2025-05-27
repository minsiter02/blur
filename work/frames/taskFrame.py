import random
from tkinter import Frame,Button,Canvas
from work.utils.file import open_image, return_resize_tkimg
from work.utils.tools import rgb_to_hex,find_element_idx
from work.utils.image_process import blur

class TaskFrame(Frame):
    def __init__(self, parent, main):
        super().__init__(parent, height=500,background="light gray")
        self.main = main

        open_button = Button(self, text="image open", command=self.on_click_open_button)
        open_button.pack(pady=5)

        self.task_canvas = Canvas(self,width=0,height=0,highlightthickness=0)
        self.task_canvas.place(relx=0.5, rely=0.52, anchor="center")

        self.task_canvas.bind("<ButtonPress-1>", self.on_press)
        self.task_canvas.bind("<B1-Motion>", self.on_drag)
        self.task_canvas.bind("<ButtonRelease-1>", self.on_release)

        self.start_x = None
        self.start_y = None
        self.shape = "rect"
        self.intensity = 121

        self.shape_history = [] #[ [id, [values]], [id, [values]], ... , [id, [values]] ] # values = [type, coords, fill_color]
        self.shape_hist_id = -1
        self.kv_tmp = []

    def on_click_open_button(self):  # 클릭 함수 이미지를 교체 함.
        image = open_image()
        if image is None:
            pass
        else:
            # main 을 거쳐 각 frame 이미지를 업데이트
            tk_image = return_resize_tkimg(image) # 리사이즈 된 Canvas 전용 이미지
            self.main.update_task_view(tk_image)
            self.main.update_preview(tk_image)
            self.shape_hist_id = 0
            self.shape_history =[[0, 0]]

    def redo_shape(self): # 임시 undo 함수.
        cur_id = self.shape_hist_id
        history = self.shape_history
        if cur_id == 0: #초기 이미지일때 지우기 안됨.
            pass
        else: # 파일구조가 조금 복잡해서 (시간순으로 정렬하려다 보니) id로 해당 index를 찾고, 그 전 index를 구하는 방식으로 구현
            cur_id_pos = find_element_idx(cur_id,history)  # 현재 id의 위치
            target_id_pos = cur_id_pos - 1  # 1칸 왼쪽의 위치
            self.task_canvas.delete(history[cur_id_pos][0])  # 사각형 삭제
            self.shape_hist_id = history[target_id_pos][0]  # 그 전 id를 현재 id

    def undo_shape(self):
        cur_id = self.shape_hist_id
        history = self.shape_history
        if cur_id == history[-1][0]:
            pass
        else: # 파일구조가 조금 복잡해서 (시간순으로 정렬하려다 보니) id로 해당 index를 찾고, 그 전 index를 구하는 방식으로 구현
            cur_id_pos = find_element_idx(cur_id,history)  # 현재 id의 위치
            target_id_pos = cur_id_pos + 1  # 1칸 왼쪽의 위치

            tg_start_x, tg_start_y, tg_end_x, tg_end_y = history[target_id_pos][1][1]
            tg_color = history[target_id_pos][1][2]

            if history[target_id_pos][1][0] == "rect": # 기존 도형 구분
                # 이미지와는 다르게 되돌리기 할 때마다 새로운 도형을 만들기 때문에 id가 바뀜.
                self.shape_history[target_id_pos][0] = self.task_canvas.create_rectangle(tg_start_x, tg_start_y, tg_end_x, tg_end_y, fill=tg_color, outline="blue", width=2)
            else:
                self.shape_history[target_id_pos][0] = self.task_canvas.create_oval(tg_start_x, tg_start_y, tg_end_x, tg_end_y, fill=tg_color, outline="red", width=2)

            self.shape_hist_id = history[target_id_pos][0]  # 되돌리기 한 id를 현재 id로 업데이트
        return self.shape_hist_id # 새로운 id를 리턴.

    def on_press(self, event): #마우스를 처음 누룰 때 시작 좌표 설정
        self.start_x = event.x
        self.start_y = event.y
        #self.blur_config 는 도형의 식별자임.
        rgb = [random.randint(0, 255) for _ in range(3)] # 지금은 랜덤: 세기, 모양에 따라 달라지도록 구현
        self.kv_tmp = [] #임시로 저장
        if self.shape == "rect":
            self.kv_tmp.append(self.task_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, fill=rgb_to_hex(rgb), outline="blue", width=2))
            self.kv_tmp.append(["rect"])
        else:
            self.kv_tmp.append(self.task_canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, fill=rgb_to_hex(rgb), outline="red", width=2))
            self.kv_tmp.append(["circle"])

    def on_drag(self, event): # 드래그 중일 때
        e_id = self.kv_tmp[0]
        self.task_canvas.coords(e_id , self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event): # 드래그 완료 후 도형 확정
        e_id, e_shape = self.kv_tmp
        #이전에 redo 여부 확인
        if self.shape_hist_id == self.shape_history[-1][0]: # 없을 시 새로운 도형 정보 추가
            self.shape_history.append(self.kv_tmp)
        else: # 이전에 redo 있을시
            cur_id_pos =find_element_idx(self.shape_hist_id, self.shape_history)  # 현재 id의 위치
            self.shape_history = self.shape_history[:cur_id_pos + 1] # redo 한 부분까지만 슬라이싱
            self.shape_history.append(self.kv_tmp) # 마지막에 새로운 도형 정보 추가

        if self.start_x == event.x or self.start_y == event.y: # 바로 놓을 경우 pass
            pass
        else:
            self.task_canvas.coords(e_id, self.start_x, self.start_y, event.x, event.y)
            coords = [self.start_x,self.start_y,event.x,event.y]
            ### 다른 방향으로 드래그시 좌표 스와핑
            if self.start_x > event.x:
                coords[0], coords[2] = coords[2], coords[0]
            if self.start_y > event.y:
                coords[1], coords[3] = coords[3], coords[1]

            self.shape_history[-1][1].append(self.task_canvas.coords(e_id)) # 기존에 그린 모양의 좌표 저장
            self.shape_history[-1][1].append(self.task_canvas.itemcget(e_id, "fill")) # 색 저장
            # blur_config 리스트에 id, shape, intensity 저장
            blur_config = [self.shape_history[-1][0] , self.shape_history[-1][1][0], self.intensity] # 왜 이러는지는 모르겠으나 이래야만 함...
            self.shape_hist_id = e_id

            image = blur(coords= coords, blur_config =blur_config) #블러 함수 호출

            preview_img = return_resize_tkimg(image) # 리사이즈 된 Canvas 전용 이미지
            self.main.update_preview(preview_img)
