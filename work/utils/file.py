from tkinter import filedialog
from PIL import Image,ImageTk
import cv2

def openfile(): #파일 열고, tk 형태로 변환.
    filepath = filedialog.askopenfilename(
        filetypes=(('Image files', '*.jpg *.png'), ('All files', '*.*')))
    image = cv2.imread(filepath)
    image = cv2.resize(image,(image.shape[1]//3,image.shape[0]//3)) #resize 관련 기능 추가해서 일정하게 보이게 하기.
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image=image)
    return image