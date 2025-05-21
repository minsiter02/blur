import cv2

class ImageProcess:
    image = None
    image_scale = None


def image_resize(img):
    img_x, img_y = img.shape[1], img.shape[0]
    img_scale = img_x / 300.0
    if img_y / img_scale > 450:  # 이미지가 너무 길면 세로를 기준으로 줄임.
        img_scale = img_y/450.0
    img_x , img_y = int(round(img_x/img_scale,3 )) , int(round(img_y / img_scale, 3))
    ImageProcess.image_scale = int(round(img_scale,3)) # class 변수 변경
    resized_img = cv2.resize(img,(img_x,img_y))
    return resized_img

