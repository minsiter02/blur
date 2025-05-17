from tkinter import filedialog
from PIL import Image,ImageTk
import cv2

class ImageProcess:
    image = None

    def openfile(self): #파일 열고, tk 형태로 변환.
        filepath = filedialog.askopenfilename( title="Select file",
            filetypes=(('Image files', '*.jpg *.png'), ('All files', '*.*')))
        image = cv2.imread(filepath)
        ImageProcess.image = image
        resized_image = cv2.resize(image,(image.shape[1]//3,image.shape[0]//3)) #resize 관련 기능 추가해서 일정하게 보이게 하기.
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
            qul.append((cv2.IMWRITE_PNG_COMPRESSION, 2)) if img_format == "PNG" \
                else write_qul.append((cv2.IMWRITE_JPEG_QUALITY, 80))
        elif qul == "middle":
            write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 4)) if img_format == "PNG" \
                else write_qul.append((cv2.IMWRITE_JPEG_QUALITY, 60))
        else: qul.append((cv2.IMWRITE_PNG_COMPRESSION, 7)) if img_format == "PNG" \
                else write_qul.append((cv2.IMWRITE_JPEG_QUALITY, 30))

        # 확장자 여부 확인 및 추가
        filename = filedialog.asksaveasfilename( title="Save Image", filetypes=file_types)
        if not(filename[-4:] == ".png" or filename[-4:] == ".jpg"):
            filename = filename + ".png" if img_format == "PNG" else filename + "jpg"
        # 파일 저장
        cv2.imwrite(filename=filename,img=ImageProcess.image,params=write_qul[0])
