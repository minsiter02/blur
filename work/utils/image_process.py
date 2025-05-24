import math
import cv2
import numpy as np


class ImageProcess:
    image = None
    image_scale = None
    img_history = []  # [ [id, image],[id, image], ... , [id, image] ]


def image_resize(img):
    img_x, img_y = img.shape[1], img.shape[0]
    if img_x <= 300 and img_y <= 450:  # 이미지가
        resized_img = img
        ImageProcess.image_scale = 1
    else:
        img_scale = img_x / 300.0
        if img_y / img_scale > 450:  # 이미지가 너무 길면 세로를 기준으로 줄임.
            img_scale = img_y / 450.0
        img_x, img_y = int(round(img_x / img_scale, 3)), int(round(img_y / img_scale, 3))
        ImageProcess.image_scale = int(round(img_scale, 3))  # class 변수 변경
        resized_img = cv2.resize(img, (img_x, img_y))
    return resized_img


def blur(coords, blur_config, intensity=121):
    blur_id, blur_shape = blur_config
    blur_img = ImageProcess.image
    start_x, start_y, end_x, end_y = [c * ImageProcess.image_scale for c in coords]  # scale에 따른 좌표 보정
    roi = blur_img[start_y:end_y, start_x:end_x]  # 관심영역만 가져오기. 행, 열
    roi_size = roi.shape[:2]  # 관심 영역의 너비, 높이 슬라이싱

    t = intensity
    data = [1 / t for _ in range(t)]
    blur_mask = np.array(data, np.float32).reshape(int(math.sqrt(t)), int(math.sqrt(t)))
    blur_roi = pixel_blur(roi, blur_mask)
    dst = []

    if blur_shape == "circle":
        pt = [r // 2 for r in roi_size[::-1]]  # x,y 좌표로 중심 점 및 타원의 크기 슬라이싱

        # fg_pass_mask 생성
        fg_pass_mask = np.zeros(roi_size)
        cv2.ellipse(fg_pass_mask, pt, pt, 0, 0, 360, (255, 255, 255), -1)  # 타원 그리기
        fg_pass_mask = cv2.split(fg_pass_mask)[0].astype("uint8")
        # bg_pass_mask 생성
        bg_pass_mask = cv2.bitwise_not(fg_pass_mask)

        background = cv2.bitwise_or(roi, roi, mask=bg_pass_mask)
        foreground = cv2.bitwise_or(blur_roi, blur_roi, mask=fg_pass_mask)
        dst = cv2.add(background, foreground)

    elif blur_shape == "rect":
        dst = blur_roi

    blur_img[start_y:end_y, start_x:end_x] = dst
    ImageProcess.image = blur_img

    img_key_value = [blur_id, blur_img]  # 순차적으로 생긴 것 들을 접근하기 위해 리스트로 구현.
    ImageProcess.img_history.append(img_key_value)
    print(ImageProcess.img_history)
    return blur_img


def pixel_blur(image, mask):
    """
    rows, cols = image.shape[:2]
    xcenter,ycenter = mask.shape[1]//2,mask.shape[0]//2
    # b,g,r 채널 분리 후 실행.
    b_dst = np.zeros((rows,cols),np.float32)
    g_dst = np.zeros((rows, cols), np.float32)
    r_dst = np.zeros((rows, cols), np.float32)
    b,g,r = cv2.split(image)

    #### 3채널 전부 마스크 적용 ####
    for i in range(ycenter, rows - ycenter):
        for j in range(xcenter, cols - xcenter):
            y1,y2 = i -ycenter, i + ycenter + 1
            x1, x2 = j - xcenter, j + xcenter + 1
            roi = b[y1:y2,x1:x2].astype("float32")

            tmp = cv2.multiply(roi,mask)
            b_dst[i,j] = cv2.sumElems(tmp)[0]

    for i in range(ycenter, rows - ycenter):
        for j in range(xcenter, cols - xcenter):
            y1,y2 = i -ycenter, i + ycenter + 1
            x1, x2 = j - xcenter, j + xcenter + 1
            roi = g[y1:y2,x1:x2].astype("float32")

            tmp = cv2.multiply(roi,mask)
            g_dst[i,j] = cv2.sumElems(tmp)[0]

    for i in range(ycenter, rows - ycenter):
        for j in range(xcenter, cols - xcenter):
            y1,y2 = i -ycenter, i + ycenter + 1
            x1, x2 = j - xcenter, j + xcenter + 1
            roi = r[y1:y2,x1:x2].astype("float32")

            tmp = cv2.multiply(roi,mask)
            r_dst[i,j] = cv2.sumElems(tmp)[0]

    # 3채널 이미지 병합 후 리턴
    return cv2.merge((b_dst.astype("uint8"),g_dst.astype("uint8"),r_dst.astype("uint8")))
    """
    return cv2.filter2D(image, -1, mask)  # 성능 문제로 OpenCV 함수 사용.