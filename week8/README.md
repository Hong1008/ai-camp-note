# Week 8: On-Device Computer Vision with MediaPipe

8주차 학습을 시작합니다. 이번 주차에는 **Google의 경량 온디바이스 컴퓨터 비전 프레임워크인 MediaPipe를 활용하여 얼굴 감지, 핸드 트래킹, 자세 감지 등 핵심 인체 랜드마크 인식 파이프라인**을 깊이 있게 다룹니다.

---

## 🗓️ 학습 로드맵

### 🟡 Theme 22: MediaPipe 프레임워크 기초 및 얼굴 인식 (2026-05-18)
MediaPipe의 동작 원리(파이프라인 및 그래프 구조)를 이해하고, 단일 이미지 및 실시간 영상 스트림에서 얼굴 및 정밀 랜드마크를 추출하는 방법을 학습합니다.

- **핵심 키워드**: MediaPipe, On-Device Vision, Face Detection, Face Mesh (468/478 Landmarks), OpenCV Integration
- **주요 실습**:
    - **Face Detection Pipeline**: 경량 모바일 블레이즈페이스(BlazeFace) 모델을 활용한 바운딩 박스 및 핵심 랜드마크 검출
    - **Face Mesh Visualization**: 468개 정밀 3D 좌표를 추출하여 실시간 얼굴 굴곡 렌더링 및 응용 서비스 구현

### 🟣 Theme 23: 인체 관절 추적 및 실시간 행동 분석
손가락 관절과 전신 랜드마크를 추적하여 공간 상의 좌표 변화를 감지하고, 이를 응용하여 제스처 인식 및 자세 교정 등의 비즈니스 모델을 구상합니다.

- **핵심 키워드**: Hand Tracking (21 Joints), Pose Estimation (33 Joints), Gesture Recognition, Coordinate Vector Analysis
- **주요 실습**:
    - **Hand Joint Mapping**: 손가락 21개 관절의 공간 좌표 값을 추출하여 특정 제스처(예: V자, 주먹 등) 정의 및 매핑
    - **Pose & Angle Calculation**: 전신 33개 관절 포인트 벡터를 활용하여 관절 사이의 각도 계산 (거북목 진단, 스쿼트 각도 등)

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-18.ipynb](05-18.ipynb): MediaPipe 기초 실습 (얼굴 감지, 핸드 트래킹, 자세 감지) (진행 중)
- **트러블슈팅 리포트**:
    - [2026-05-18 리포트](./troubleshooting/2026-05-18.md): PaddleOCR 'paddle' 모듈 누락 및 uv 의존성 충돌 해결 리포트 (완료)

---

## 🛠️ 사용 기술 및 의존성
- **Framework & Libraries**: `MediaPipe`, `OpenCV (cv2)`, `NumPy`, `Matplotlib`
- **Models**: BlazeFace, FaceMesh, MediaPipe Hands, MediaPipe Pose
- **Key Techniques**: Real-time Video Stream Processing, Landmark Coordinate Vector Analysis, Mathematical Pose Evaluation (Cosine Similarity / Angles)
