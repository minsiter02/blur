import random
from tkinter import Frame,Canvas
from tkinter.ttk import Button
from work.utils.file import open_image, return_resize_tkimg
from work.utils.tools import blur_to_color,find_element_idx
from work.utils.image_process import blur


class TaskFrame(Frame):
    def __init__(self, parent, main):
        super().__init__(parent, height=500)
        self.main = main

        open_button = Button(self, text="open image", command=self.on_click_open_button)
        open_button.pack(pady=5)

        # 일정한 테두리 위해 프레임 추가
        self.canvas_frame = Frame(self)
        self.canvas_frame.place(relx=0.5, rely=0.54, anchor="center")
        self.task_canvas = Canvas(self.canvas_frame,width=0,height=0,highlightthickness=0)
        self.task_canvas.pack()

        self.task_canvas.bind("<ButtonPress-1>", self.on_press)
        self.task_canvas.bind("<B1-Motion>", self.on_drag)
        self.task_canvas.bind("<ButtonRelease-1>", self.on_release)

        self.task_canvas_width = self.task_canvas_height = self.start_x = self.start_y = self.end_x = self.end_y = None
        self.shape = "rect"
        self.intensity = 121

        # [ [id, [values]], [id, [values]], ... , [id, [values]] ] # values = [type, coords, fill_color]
        self.shape_history = []
        self.shape_hist_id = -1
        self.kv_tmp = []

        self.press_shift = False

    def on_click_open_button(self):  # 클릭 함수 이미지를 교체 함.
        image = open_image()
        if image is None: return None

        # main 을 거쳐 각 frame 이미지를 업데이트
        tk_image = return_resize_tkimg(image) # 리사이즈 된 Canvas 전용 이미지
        self.main.update_task_view(tk_image)
        self.main.update_preview(tk_image)
        self.shape_hist_id = 0
        self.shape_history =[[0, 0]]
        self.task_canvas_width = self.task_canvas.winfo_width()
        self.task_canvas_height = self.task_canvas.winfo_height()


    def undo_shape(self):
        cur_id = self.shape_hist_id
        history = self.shape_history
        if cur_id == 0: return  #초기 이미지 지우기 안됨.
         # 파일 구조가 조금 복잡해서 (시간순으로 정렬하려다 보니) id로 해당 index를 찾고, 그 전 index를 구하는 방식으로 구현
        cur_id_pos = find_element_idx(cur_id,history)  # 현재 id의 위치
        target_id_pos = cur_id_pos - 1  # 1칸 왼쪽의 위치
        self.task_canvas.delete(history[cur_id_pos][0])  # 사각형 삭제
        self.shape_hist_id = history[target_id_pos][0]  # 그 전 id를 현재 id

    def redo_shape(self):
        cur_id = self.shape_hist_id
        history = self.shape_history
        if cur_id == history[-1][0]: return None  # 마지막 기록이 지금 id와 같으면 수행 안 함
         # 파일 구조가 조금 복잡: (스택 구조로 구현 하려다 보니) id로 해당 index 추출, 그 앞의 index 구하는 방식
        cur_id_pos = find_element_idx(cur_id,history)  # 현재 id의 위치
        target_id_pos = cur_id_pos + 1  # 1칸 왼쪽의 위치

        tg_start_x, tg_start_y, tg_end_x, tg_end_y = history[target_id_pos][1][1]
        tg_color = history[target_id_pos][1][2]

        if history[target_id_pos][1][0] == "rect": # 기존 도형 구분
            # 이미지와는 다르게 redo 할 때마다 새로운 도형을 만들기 때문에 id가 바뀜.
            self.shape_history[target_id_pos][0] = self.task_canvas.create_rectangle(tg_start_x, tg_start_y, tg_end_x, tg_end_y, fill=tg_color, outline="blue", width=1)
        else:
            self.shape_history[target_id_pos][0] = self.task_canvas.create_oval(tg_start_x, tg_start_y, tg_end_x, tg_end_y, fill=tg_color, outline="red", width=1)

        self.shape_hist_id = history[target_id_pos][0]  # 되돌리기 한 id를 현재 id로 업데이트
        return self.shape_hist_id # 새로운 id를 리턴.


    def on_press(self, event): #마우스를 처음 누룰 때 시작 좌표 설정
        self.start_x = event.x
        self.start_y = event.y
        #self.blur_config 는 도형의 식별자임.
        rgb = [random.randint(0, 255) for _ in range(3)] # 지금은 랜덤: 세기, 모양에 따라 달라지도록 구현
        self.kv_tmp = [] # 임시로 저장
        if self.shape == "rect":
            self.kv_tmp.append(self.task_canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, fill=blur_to_color( intensity=self.intensity), outline="blue", width=1))
            self.kv_tmp.append(["rect"])
        else:
            self.kv_tmp.append(self.task_canvas.create_oval(self.start_x, self.start_y, self.start_x, self.start_y, fill=blur_to_color(intensity=self.intensity), outline="red", width=1))
            self.kv_tmp.append(["circle"])


    def on_drag(self, event): # 드래그 중일 때
        e_id = self.kv_tmp[0]
        # 이벤트 중에 좌표 범위 제한
        event.x = max(1, min(event.x, self.task_canvas_width))
        event.y = max(1, min(event.y, self.task_canvas_height))

        self.end_x = max(1, min(event.x, self.task_canvas_width))
        self.end_y = max(1, min(event.y, self.task_canvas_height))

        if self.press_shift:  # Shift 키를 눌렀을 때 정사각형 유지
            width = abs(self.end_x - self.start_x)
            height = abs(self.end_y - self.start_y)
            size = min(width, height)  # 가로, 세로 중 작은 값으로 크기 설정
            if self.start_x > self.end_x: # x좌표
                self.end_x = max(1, self.start_x - size)
            else:
                self.end_x = min(self.start_x + size, self.task_canvas_width)
            # y좌표
            if self.start_y > self.end_y:
                self.end_y = max(1, self.start_y - size)
            else:
                self.end_y = min(self.start_y + size, self.task_canvas_height)
            self.task_canvas.coords(e_id, self.start_x, self.start_y, self.end_x, self.end_y)

        else: # Shift를 누르지 않은 경우
            self.end_y = max(1, min(event.y, self.task_canvas_height))
            self.task_canvas.coords(e_id, self.start_x, self.start_y, event.x, self.end_y)


    def on_release(self, event): # 드래그 완료 후 도형 확정
        e_id, e_shape = self.kv_tmp
        if self.start_x == event.x or self.start_y == event.y: # 바로 놓을 경우 pass
            self.task_canvas.delete(self.kv_tmp[0])
            return None
        # 이전에 redo 여부 확인
        if self.shape_hist_id == self.shape_history[-1][0]: # 없을 시 새로운 도형 정보 추가
            self.shape_history.append(self.kv_tmp)
        else: # 이전에 redo 있을시
            cur_id_pos =find_element_idx(self.shape_hist_id, self.shape_history)  # 현재 id의 위치
            self.shape_history = self.shape_history[:cur_id_pos + 1] # redo 한 부분까지만 슬라이싱
            self.shape_history.append(self.kv_tmp) # 마지막에 새로운 도형 정보 추가

        self.end_x = max(1, min(event.x, self.task_canvas_width))
        self.end_y = max(1, min(event.y, self.task_canvas_height))

        if self.press_shift:  # Shift 키를 누른 경우 정사각형 유지
            width = abs(self.end_x - self.start_x)
            height = abs(self.end_y - self.start_y)
            size = min(width, height)  # 가로, 세로 중 작은 값 선택

            if self.start_x > self.end_x:
                self.end_x = max(1, self.start_x - size)
            else:
                self.end_x = min(self.start_x + size, self.task_canvas_width)

            if self.start_y > self.end_y:
                self.end_y = max(1, self.start_y - size)
            else:
                self.end_y = min(self.start_y + size, self.task_canvas_height)

        self.task_canvas.coords(e_id, self.start_x, self.start_y, self.end_x, self.end_y)
        coords = [self.start_x,self.start_y,self.end_x,self.end_y]
        ### 다른 방향으로 드래그시 좌표 스와핑
        if self.start_x > self.end_x:
            coords[0], coords[2] = coords[2], coords[0]
        if self.start_y > self.end_y:
            coords[1], coords[3] = coords[3], coords[1]

        self.shape_history[-1][1].append(self.task_canvas.coords(e_id)) # 기존에 그린 모양의 좌표 저장
        self.shape_history[-1][1].append(self.task_canvas.itemcget(e_id, "fill")) # 색 저장
        # blur_config 리스트에 id, shape, intensity 저장
        blur_config = [self.shape_history[-1][0] , self.shape_history[-1][1][0], self.intensity] # 왜 이러는지는 모르겠으나 이래야만 함...
        self.shape_hist_id = e_id

        image = blur(coords= coords, blur_config =blur_config) #블러 함수 호출

        preview_img = return_resize_tkimg(image) # 리사이즈 된 Canvas 전용 이미지
        self.main.update_preview(preview_img)