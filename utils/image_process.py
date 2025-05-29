import math
import cv2
import numpy as np
from utils.tools import find_element_idx

class ImageProcess:
    image = image_scale = None
    img_history = []  # [ [id, image],[id, image], ... , [id, image] ]
    img_history_id = -1

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
        ImageProcess.image_scale =round(img_scale, 3)  # class 변수 변경
        resized_img = cv2.resize(img, (img_x, img_y))
    return resized_img

def undo_img():
    cur_id = ImageProcess.img_history_id #현재 id
    history = ImageProcess.img_history #
    if cur_id == 0 or cur_id == -1: #초기 이미지일때 지우기 안됨.
        return None
    else:# 파일구조가 조금 복잡해서 (시간 순으로 정렬 하려다 보니) id로 해당 index를 찾고, 그 전 index를 구하는 방식으로 구현
        cur_id_pos = find_element_idx(cur_id,history) #현재 id의 위치
        target_id_pos = cur_id_pos - 1 # 1칸 왼쪽의 위치
        ImageProcess.image = history[target_id_pos][1] # 그 전 이미지 불러오기
        ImageProcess.img_history_id = history[target_id_pos][0] # 그 전
        return ImageProcess.image

def redo_img():
    cur_id = ImageProcess.img_history_id
    history = ImageProcess.img_history
    if cur_id == -1 or cur_id == history[-1][0]:
        return None
    else:
        cur_id_pos = find_element_idx(cur_id,history) # 현재 id의 위치
        target_id_pos = cur_id_pos + 1  # 1칸 오른쪽의 위치
        ImageProcess.image = history[target_id_pos][1]
        ImageProcess.img_history_id = history[target_id_pos][0]
        return ImageProcess.image

def update_redo_id(redo_id):
    cur_id_pos = find_element_idx(ImageProcess.img_history_id,ImageProcess.img_history) # 현재 id의 위치를 찾고
    ImageProcess.img_history[cur_id_pos][0] = redo_id # 기록에서 해당 위치에 새로운 id 업데이트
    ImageProcess.img_history_id = redo_id # 현재 id를 업데이트


def blur(coords, blur_config):
    blur_id, blur_shape, intensity = blur_config
    blur_img = ImageProcess.image.copy() # 참조가 아닌 복사
    start_x, start_y, end_x, end_y = [int(round(c * ImageProcess.image_scale)) for c in coords]  # scale에 따른 좌표 보정
    roi = blur_img[start_y:end_y, start_x:end_x]  # 관심영역만 가져오기. 행, 열
    roi_size = roi.shape[:2]  # 관심 영역의 너비, 높이 슬라이싱

    data = [1 / intensity for _ in range(intensity)]
    blur_mask = np.array(data, np.float32).reshape(int(math.sqrt(intensity)), int(math.sqrt(intensity)))
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

    img_id_value = [blur_id, blur_img]
    # 순차적으로 생긴 것 들을 접근하기 위해 리스트로 구현.
    if ImageProcess.img_history_id == ImageProcess.img_history[-1][0]: #만약 마지막 원소의 id와 현재 이미지 id가 같다면
        ImageProcess.img_history.append(img_id_value) # 그냥 맨 뒤에 id,이미지 정보 추가
    else:
        # redo 기록이 있다면 (마지막 원소가 아니라면) redo 부분까지만 슬라이싱
        cur_id_pos = find_element_idx(ImageProcess.img_history_id,ImageProcess.img_history)
        ImageProcess.img_history = ImageProcess.img_history[:cur_id_pos + 1]
        ImageProcess.img_history.append(img_id_value) # redo 부분 이후로 지우고 거기다가 추가.

    ImageProcess.img_history_id = ImageProcess.img_history[-1][0]

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