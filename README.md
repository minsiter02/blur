# 🖼️ Blur - Image Blur Tool

**이미지에서 얼굴 및 특정 영역을 자동/수동으로 블러 처리할 수 있는 Python GUI 어플리케이션입니다.**

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)](https://opencv.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## ✨ 주요 기능

- 🤖 **자동 얼굴 블러**: Haar Cascade 기반 얼굴 자동 인식 및 블러 처리
- ✏️ **수동 영역 블러**: 마우스 드래그로 사각형/원형 영역 선택 및 블러 적용
- 🎨 **블러 강도 조절**: 슬라이더를 통한 실시간 블러 강도 조정
- 🔄 **Undo/Redo**: 작업 히스토리 기반 되돌리기/다시 실행 기능
- 👁️ **실시간 미리보기**: 블러 작업 결과를 즉시 확인
- 💾 **이미지 저장**: 블러 처리된 이미지 다운로드

## 📦 설치 방법

### 필수 요구사항

- Python 3.7 이상

### 실행 방법
```
git clone https://github.com/minsiter02/blur.git

cd blur

python main.py
```

## 🎮 사용법

### 기본 조작

1. **이미지 열기**: `Ctrl+F` 또는 왼쪽 상단의 Open 버튼 클릭
2. **영역 선택**: 마우스 드래그로 블러 처리할 영역 선택
3. **블러 타입 변경**: Tab 키 또는 하단 라디오 버튼으로 사각형/원형 전환
4. **블러 강도 조절**: 슬라이더 또는 `A`/`D` 키로 강도 조정
5. **자동 얼굴 블러**: `R` 키 또는 Auto 버튼 클릭
6. **이미지 저장**: `Ctrl+S` 또는 우측 하단의 Download 버튼 클릭

### ⌨️ 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+F` | 이미지 열기 |
| `Ctrl+S` | 이미지 저장 |
| `Ctrl+Z` | 되돌리기 (Undo) |
| `Ctrl+Y` | 다시 실행 (Redo) |
| `Tab` | 블러 타입 전환 (사각형 ↔ 원형) |
| `A` | 블러 강도 감소 |
| `D` | 블러 강도 증가 |
| `R` | 자동 얼굴 블러 실행 |
| `Shift` | 드래그 시 정사각형/정원 유지 |

## 📁 프로젝트 구조


## 🎮 사용법

### 기본 조작

1. **이미지 열기**: `Ctrl+F` 또는 왼쪽 상단의 Open 버튼 클릭
2. **영역 선택**: 마우스 드래그로 블러 처리할 영역 선택
3. **블러 타입 변경**: Tab 키 또는 하단 라디오 버튼으로 사각형/원형 전환
4. **블러 강도 조절**: 슬라이더 또는 `A`/`D` 키로 강도 조정
5. **자동 얼굴 블러**: `R` 키 또는 Auto 버튼 클릭
6. **이미지 저장**: `Ctrl+S` 또는 우측 하단의 Download 버튼 클릭

### ⌨️ 단축키

| 단축키 | 기능 |
|--------|------|
| `Ctrl+F` | 이미지 열기 |
| `Ctrl+S` | 이미지 저장 |
| `Ctrl+Z` | 되돌리기 (Undo) |
| `Ctrl+Y` | 다시 실행 (Redo) |
| `Tab` | 블러 타입 전환 (사각형 ↔ 원형) |
| `A` | 블러 강도 감소 |
| `D` | 블러 강도 증가 |
| `R` | 자동 얼굴 블러 실행 |
| `Shift` | 드래그 시 정사각형/정원 유지 |

## 📁 프로젝트 구조
```
blur/
├── main.py # 메인 GUI 어플리케이션
├── frames/ # GUI 프레임 컴포넌트
│ ├── taskFrame.py # 이미지 작업 프레임 (블러 작업 영역)
│ ├── previewFrame.py # 미리보기 프레임
│ ├── arrowFrame.py # UI 구성용 화살표 프레임
│ ├── toolsFrame.py # 도구 프레임 (버튼, 슬라이더)
│ └── ImageSettingsWindow.py # 이미지 설정 윈도우
├── utils/ # 유틸리티 함수
│ ├── image_process.py # 이미지 처리 로직 (블러링, 얼굴 탐지)
│ ├── file.py # 파일 입출력 처리
│ ├── tools.py # 기타 도구 함수
│ └── haarcascade_frontalface_default.xml # 얼굴 탐지 모델
└── theme/ # GUI 테마 파일
└── azure.tcl # Azure 테마
```

## 🛠️ 기술 스택

- **GUI Framework**: Tkinter, ttk
- **Image Processing**: OpenCV (cv2)
- **Face Detection**: Haar Cascade Classifier
- **Array Processing**: NumPy

## 🎨 주요 기능 상세

### 1. 자동 얼굴 블러
- Haar Cascade Classifier를 사용한 얼굴 자동 탐지
- 탐지된 모든 얼굴에 자동으로 블러 적용
- 얼굴별 개별 Undo/Redo 지원

### 2. 수동 블러
- **사각형 블러**: 드래그로 사각형 영역 선택
- **원형 블러**: 원형 마스크를 적용한 자연스러운 블러
- **Shift 키**: 정사각형 또는 정원 그리기

### 3. 히스토리 관리
- 모든 블러 작업을 히스토리에 저장
- Undo/Redo를 통한 작업 되돌리기 및 복원
- 히스토리 분기 처리 (새 작업 시 이후 히스토리 제거)

### 4. 이미지 스케일링
- 큰 이미지 자동 리사이징 (최대 300x450 기준)
- 원본 이미지 비율 유지
- 저장 시 원본 해상도로 복원

## 🤝 기여하기

이 프로젝트에 기여하고 싶으시다면:

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 👤 작성자

**minsiter02**

- GitHub: [@minsiter02](https://github.com/minsiter02)

## 🙏 감사의 말

- OpenCV 커뮤니티
- Azure 테마 제작자

---

⭐ 이 프로젝트가 도움이 되셨다면 Star를 눌러주세요!
