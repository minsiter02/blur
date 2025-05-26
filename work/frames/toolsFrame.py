from tkinter import Frame, Button, Scale, Radiobutton, IntVar
from work.utils.image_process import redo_img
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

        self.radio_var = IntVar()
        self.rdo_rect = Radiobutton(self, text="Rectangle", variable=self.radio_var, value=1)
        self.rdo_circle = Radiobutton(self, text="Circle", variable=self.radio_var, value=2)

        self.rdo_rect.pack(side="left", padx=5)
        self.rdo_circle.pack(side="left", padx=5)

        self.scale = Scale(self, variable=1.0, command=self.select, orient="horizontal", showvalue=False)
        self.scale.pack(side="right", padx=10)

    def select(self, event):
        print(event)

    def on_click_redo_btn(self):
        redo_image = redo_img()
        if redo_image is None:
            pass
        else:
            img = return_resize_tkimg(redo_image)
            self.main.update_preview(img)
            self.main.redo_task()


    def on_click_undo_btn(self):
        print()