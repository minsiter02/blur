from tkinter import filedialog

from PIL import Image,ImageTk
import cv2

class ImageProcess:
    image = None
    image_scale = None

    def openfile(self): #파일 열고, tk 형태로 변환.
        filepath = filedialog.askopenfilename( title="Select file",
            filetypes=(('Image files', '*.jpg *.png'), ('All files', '*.*')))
        image = cv2.imread(filepath)
        ImageProcess.image = image
        resized_image = self.image_resize(img=image)
        preview_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        preview_image = Image.fromarray(preview_image) #Numpy image to PIL image
        preview_image = ImageTk.PhotoImage(image=preview_image) #PIL image to Tk image
        return preview_image

    def savefile(self,img_format, qul): #넘겨 받은 포맷, 퀄리티로 지정한 경로에 저장
        file_types = []
        write_qul =[]
        if img_format == "PNG":
            file_types.append(('PNG files', '*.png'))
        elif img_format == "JPG":
            file_types.append(('JPG files', '*.jpg'))

        # 포맷 퀄리티 params 선택
        if qul == "high":
                write_qul.append((cv2.IMWRITE_PNG_COMPRESSION,0)) if img_format == "PNG" else write_qul.append((cv2.IMWRITE_JPEG_QUALITY,100))
        elif qul == "normal":
            write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 2)) if img_format == "PNG" else write_qul.append((cv2.IMWRITE_JPEG_QUALITY, 80))
        elif qul == "middle":
            write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 4)) if img_format == "PNG" else write_qul.append((cv2.IMWRITE_JPEG_QUALITY, 60))
        elif qul == "low": write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 8)) if img_format == "PNG" else write_qul.append((cv2.IMWRITE_JPEG_QUALITY, 30))

        # 저장시 파일명 확장자 여부 확인 및 추가
        filepath = filedialog.asksaveasfilename( title="Save Image", filetypes=file_types)
        if not(filepath[-4:] == ".png" or filepath[-4:] == ".jpg"):
            filepath = filepath + ".png" if img_format == "PNG" else filepath + "jpg"

        # 파일 저장
        if ImageProcess.image is None or filepath == ".png" == filepath != ".jpg":
            pass # None이거나 경로가 비었을 경우 안 함.
        else:
            cv2.imwrite(filename=filepath,img=ImageProcess.image,params=write_qul[0])

    def image_resize(self, img):
        img_x, img_y = img.shape[1], img.shape[0]
        width = 300
        img_scale = img_x / 300.0
        while img_y / img_scale > 450:
            img_scale = img_x / width
            width -= 0.1

        img_x , img_y = int(round(img_x/img_scale,3 )) , int(round(img_y / img_scale, 3))
        ImageProcess.image_scale = int(round(img_scale))
        resized_img = cv2.resize(img,(img_x,img_y))
        return resized_img
