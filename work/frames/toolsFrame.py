from tkinter import Frame, Button, Scale, Radiobutton, StringVar, IntVar
from work.utils.image_process import redo_img,undo_img, update_undo_id
from work.utils.file import return_resize_tkimg
class ToolsFrame(Frame):
    def __init__(self, parent, main):
        super().__init__(parent, height=60,background="gray")
        self.main = main
        top_frame = Frame(self,background="gray",pady= 5)
        top_frame.pack(side="top")

        self.redo_button = Button(top_frame, text="Redo", command=self.on_click_redo_btn)
        self.undo_button = Button(top_frame, text="Undo", command=self.on_click_undo_btn)

        self.redo_button.pack(side="left", padx=8)
        self.undo_button.pack(side="left", padx=8)

        self.radio_var = StringVar(value="rect")
        self.rdo_rect = Radiobutton(self, text="Rectangle", variable=self.radio_var, value="rect", command=self.on_rdo_btn)
        self.rdo_circle = Radiobutton(self, text="Circle", variable=self.radio_var, value="circle", command=self.on_rdo_btn)

        self.rdo_rect.pack(side="left", padx=5)
        self.rdo_circle.pack(side="left", padx=5)

        self.intensity_value = IntVar(value=15)
        self.scale = Scale(self,width=20, length=600, troughcolor="light gray",sliderlength=15 , relief="flat",sliderrelief="flat", variable=self.intensity_value,  orient="horizontal", showvalue=False, from_=3, to = 27, resolution= 2, command=self.change_intensity)
        self.scale.pack(side="right", padx=10)

    def on_click_redo_btn(self):
        redo_image = redo_img()
        if redo_image is None:
            pass
        else:
            img = return_resize_tkimg(redo_image)
            self.main.update_preview(img)
            self.main.redo_task()

    def on_click_undo_btn(self):
        undo_image = undo_img()
        if undo_image is None:
            pass
        else:
            img = return_resize_tkimg(undo_image)
            self.main.update_preview(img)
            # 새로운 id를 넘겨줌.
            undo_id = self.main.undo_task()
            update_undo_id(undo_id)

    def on_rdo_btn(self):
        blur_set = [self.radio_var.get(), (self.intensity_value.get()**2)]
        self.main.change_blur_settings(blur_set)

    def change_intensity(self, event):
        print(event)
        blur_set = [self.radio_var.get(), (self.intensity_value.get()**2)]
        self.main.change_blur_settings(blur_set)
