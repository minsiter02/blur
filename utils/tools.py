import random

def find_element_idx(element,target_list):
    elements = [e[0] for e in target_list] # 내부 리스트의 첫 요소를 가진 리스트
    element_idx = elements.index(element)
    return element_idx

def blur_to_color(intensity):
    norm_intensity = (intensity - 3**2) / (35 ** 2 - 3 ** 2) # 강도 정규화
    # 강도 높을 수록 더 큰 값을 빼므로 색이 어두워 짐
    r,g,b = [random.randint(150,255)-round(norm_intensity*150) for _ in range(3)]
    return f'#{r:02x}{g:02x}{b:02x}'

