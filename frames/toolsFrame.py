from tkinter import Frame, StringVar, IntVar
from tkinter.ttk import Button, Scale, Radiobutton
from utils.image_process import redo_img,undo_img, update_redo_id
from utils.file import return_resize_tkimg
class ToolsFrame(Frame):
    def __init__(self, parent, main):
        super().__init__(parent, height=60)
        self.main = main
        top_frame = Frame(self)
        top_frame.pack(side="top")

        self.redo_button = Button(top_frame, text="Undo", command=self.on_click_undo_btn)
        self.undo_button = Button(top_frame, text="Redo", command=self.on_click_redo_btn)

        self.redo_button.pack(side="left", padx=8)
        self.undo_button.pack(side="left", padx=8)

        self.radio_var = StringVar(value="rect")
        self.rdo_rect = Radiobutton(self, text="Rectangle", variable=self.radio_var, value="rect", command=self.on_rdo_btn)
        self.rdo_circle = Radiobutton(self, text="Circle", variable=self.radio_var, value="circle", command=self.on_rdo_btn)

        self.rdo_rect.pack(side="left", padx=5)
        self.rdo_circle.pack(side="left", padx=5)

        self.intensity_value = IntVar(value=19)
        self.scale = Scale(self, length=600, variable=self.intensity_value, orient="horizontal", from_=3, to = 35, command=self.change_intensity)
        self.scale.pack(side="right", padx=10)

    def on_click_undo_btn(self): # 되돌리기 버튼
        undo_image = undo_img() # 이미지 부터 받기
        if undo_image is None: return None # 없으면 안 함
        img = return_resize_tkimg(undo_image) # 리사이즈
        self.main.update_preview(img) # 미리보기 업데이트
        self.main.undo_task() # 도형 되돌리기

    def on_click_redo_btn(self):
        redo_image = redo_img()
        if redo_image is None: return None
        img = return_resize_tkimg(redo_image)
        self.main.update_preview(img)
        # 새로운 id를 넘겨줌.
        redo_id = self.main.redo_task()
        update_redo_id(redo_id)

    def on_rdo_btn(self):
        self.main.change_blur_shape(self.radio_var.get())

    def change_intensity(self, event):
        # ttk 사용시 resolution 옵션이 불가하여 값 강제 조정
        scale_value = 3 + (round((float(event) - 3) / 2) * 2)
        self.intensity_value.set(scale_value)
        self.main.change_blur_intensity(scale_value)

