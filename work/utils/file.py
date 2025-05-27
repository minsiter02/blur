from tkinter import filedialog
import cv2
import numpy as np
from PIL import Image,ImageTk
from  work.utils.image_process import ImageProcess,image_resize

def open_image(): #파일 열기
    filepath = filedialog.askopenfilename( title="Select file",
        filetypes=(('Image files', '*.jpg *.png'), ('All files', '*.*')))
    if filepath == '': return None # 이미지 로드를 최종적으로 로드 하지 않았을 경우 None
    #image = cv2.imread(filepath)
    img_array = np.fromfile(filepath, np.uint8) # 이미지 불러오기 한글 경로 대응
    image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    ImageProcess.image = image
    ImageProcess.img_history = []
    ImageProcess.img_history = [[0,image]]
    ImageProcess.img_history_id = 0
    return image

def save_image(img_format, qul): # 넘겨 받은 포맷, 퀄리티로 지정한 경로에 저장
    file_types = []
    write_qul =[]
    if img_format == "PNG":
        file_types.append(('PNG files', '*.png'))
    elif img_format == "JPG":
        file_types.append(('JPG files', '*.jpg'))

    # 포맷 퀄리티 params 선택
    if qul == "high":
        write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 0)) if img_format == "PNG" else write_qul.append(
            (cv2.IMWRITE_JPEG_QUALITY, 100))
    elif qul == "normal":
        write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 2)) if img_format == "PNG" else write_qul.append(
            (cv2.IMWRITE_JPEG_QUALITY, 80))
    elif qul == "middle":
        write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 4)) if img_format == "PNG" else write_qul.append(
            (cv2.IMWRITE_JPEG_QUALITY, 60))
    elif qul == "low":
        write_qul.append((cv2.IMWRITE_PNG_COMPRESSION, 8)) if img_format == "PNG" else write_qul.append(
            (cv2.IMWRITE_JPEG_QUALITY, 30))

    # 저장시 파일명 확장자 여부 확인 및 추가
    filepath = filedialog.asksaveasfilename(title="Save Image", filetypes=file_types)
    if not (filepath[-4:] == ".png" or filepath[-4:] == ".jpg"):
        filepath = filepath + ".png" if img_format == "PNG" else filepath + ".jpg"

    # 파일 저장 # None이거나 경로가 비었을 경우 안 함.
    if ImageProcess.image is None or (filepath == ".png" or filepath == ".jpg"): return None
    #cv2.imwrite(filename=filepath, img=ImageProcess.image, params=write_qul[0])
    success, buffer = cv2.imencode(filepath[-4:], ImageProcess.image) # 이미지 저장 한글 경로 대응
    if success:
        with open(filepath, mode= 'wb') as f_writer:
            f_writer.write(buffer)

def return_resize_tkimg(image): #TK Canvas에 resize하여 표시하기 위해 리사이즈 까지 함.
    resized_image = image_resize(img=image)
    pil_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(pil_image)  # Numpy image to PIL image
    tk_image= ImageTk.PhotoImage(image=pil_image)  # PIL image to Tk image
    return tk_image