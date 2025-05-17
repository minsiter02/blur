from tkinter import  Label,Button,Toplevel,Radiobutton,StringVar

from work.utils.image_process import ImageProcess
class ImageSettingsWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("이미지 저장 설정")
        self.geometry("300x100+200+250")
        self.img_process = ImageProcess()
        self.grab_set()
        self.qual_var = StringVar(value="high")
        rdo_high_qual = Radiobutton(self, text="최고", value="high",variable=self.qual_var)
        rdo_normal_qual = Radiobutton(self, text="보통", value="normal", variable=self.qual_var)
        rdo_middle_qual = Radiobutton(self, text="중간", value="middle", variable=self.qual_var)
        rdo_low_qual = Radiobutton(self, text="낮음", value="low", variable=self.qual_var)

        label =Label(self,text="화질 및 파일 포맷을 선택하세요.")
        label.pack(side="top")
        rdo_high_qual.pack(side="left")
        rdo_normal_qual.pack(side="left")
        rdo_middle_qual.pack(side="left")
        rdo_low_qual.pack(side="left")

        self.sel_png_button = Button(self, text="PNG",command=self.on_click_select_format)
        self.sel_png_button.pack(side="right")
        self.sel_jpg_button = Button(self, text="JPG",command=self.on_click_select_format)
        self.sel_jpg_button.pack(side="right")

        self.wait_window(self)

    def on_click_select_format(self):
        filename =self.img_process.savefile("PNG")
        print(filename)
        ## 파일 저장하는 부분 추가!
        self.destroy()