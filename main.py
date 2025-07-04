from tkinter import  Tk
from frames.taskFrame import TaskFrame
from frames.previewFrame import PreviewFrame
from frames.arrowFrame import ArrowFrame
from frames.toolsFrame import ToolsFrame
from tkinter import ttk

class MainWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Image_Blur")
        self.geometry("800x560+100+100")
        self.resizable(False, False)  # 윈도우 크기 고정

        ###################### define frame ######################
        self.tools_frame = ToolsFrame(self, main= self)
        self.tools_frame.pack(side="bottom", expand=True, fill="both")

        self.task_frame = TaskFrame(self, main=self)
        self.task_frame.pack(side="left", expand=True, fill="both")
        self.task_frame.pack_propagate(False) # 크기고정

        arrow_frame = ArrowFrame(self)
        arrow_frame.pack(side="left", fill="both")

        self.preview_frame = PreviewFrame(self)
        self.preview_frame.pack(side="left", expand=True, fill="both")
        self.preview_frame.pack_propagate(False) # 크기고정
        ####################### end_define frame #################

        ####################### KEY_EVENT ########################
        self.bind("<KeyPress-Shift_L>", self.press_shift)
        self.bind("<KeyRelease-Shift_L>", self.release_shift)
        self.bind("<Tab>", self.on_tap)
        self.bind("<Control-z>", self.on_ctrl_z)
        self.bind("<Control-y>", self.on_ctrl_y)
        self.bind("<Control-f>", self.on_ctrl_f)
        self.bind("<Control-s>", self.on_ctrl_s)
        self.bind("<a>", self.on_a)
        self.bind("<d>", self.on_d)
        self.bind("<r>", self.on_r)
        ################### END_KEY_EVENT ########################

    def update_task_view(self,img):
        img_width = img.width()
        img_height = img.height()
        self.task_frame.canvas_frame.config(borderwidth=1,relief="solid")
        self.task_frame.task_canvas.config(width=img_width, height=img_height)
        self.task_frame.task_canvas.create_image( img_width/2, img_height/2, image=img)
        self.task_frame.task_canvas.image_names=img
        self.update_idletasks()

    def update_preview(self, img):
        img_width = img.width()
        img_height = img.height()
        self.preview_frame.canvas_frame.config(borderwidth=1,relief="solid")
        self.preview_frame.pre_canvas.config(width=img_width, height=img_height)
        self.preview_frame.pre_canvas.create_image(img_width/2, img_height/2, image=img)
        self.preview_frame.pre_canvas.image_names = img

    def undo_task(self):
        self.task_frame.undo_shape()

    def redo_task(self):
        redo_id = self.task_frame.redo_shape()
        return redo_id

    def draw_rect_face(self,id_value):
        self.task_frame.draw_rect_face(id_value=id_value)

    def change_blur_shape(self,blur_shape):
        self.task_frame.shape = blur_shape
    def change_blur_intensity(self,blur_intensity):
        self.task_frame.intensity = blur_intensity ** 2

    ####################### KEY_EVENT_CALLBACK ###############
    def press_shift(self,event):
        self.task_frame.press_shift = True
    def release_shift(self,event):
        self.task_frame.press_shift = False
    def on_tap(self,event):
        self.tools_frame.radio_var.set("rect") if self.tools_frame.radio_var.get() == "circle" else self.tools_frame.radio_var.set("circle")
        self.tools_frame.on_rdo_btn()
        return "break"
    def on_ctrl_z(self,event):
        self.tools_frame.undo_button.focus_set()
        self.tools_frame.on_click_undo_btn()
    def on_ctrl_y(self,event):
        self.tools_frame.redo_button.focus_set()
        self.tools_frame.on_click_redo_btn()
    def on_ctrl_s(self,event):
        self.preview_frame.download_button.focus_set()
        self.preview_frame.on_click_download_button()
    def on_ctrl_f(self,event):
        self.task_frame.open_button.focus_set()
        self.task_frame.on_click_open_button()
    def on_a(self,event):
        i = self.tools_frame.intensity_value.get()
        if i > 3:
            self.tools_frame.intensity_value.set(i - 2)
            self.change_blur_intensity(i)
    def on_d(self,event):
        i = self.tools_frame.intensity_value.get()
        if i < 35:
            self.tools_frame.intensity_value.set(i + 2)
            self.change_blur_intensity(i)
    def on_r(self,event):
        self.tools_frame.face_button.focus_set()
        self.tools_frame.on_click_face_btn()

main = MainWindow()
style = ttk.Style(main)
main.tk.call('source', 'theme/azure.tcl')
style.theme_use('azure')

main.mainloop()

