def rgb_to_hex(rgb):
    return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'

def find_element_idx(element,target_list):
    elements = [e[0] for e in target_list] # 내부 리스트의 첫 요소를 가진 리스트
    element_idx = elements.index(element)
    return element_idx
