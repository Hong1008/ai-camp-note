# Week 7: Deep Learning Foundations & Neural Networks

7주차 학습을 시작합니다. 이번 주차에는 **딥러닝의 기초 원리와 신경망 모델의 설계 및 학습**을 중점적으로 다룹니다.

---


## 🗓️ 학습 로드맵

### 🟡 Theme 17: 신경망의 원리 및 PyTorch 심화 (2026-05-11)
인공 신경망의 수학적 구조와 역전파(Backpropagation) 알고리즘을 이해하고, 다양한 데이터셋에 최적화된 모델링을 실습했습니다.

- **핵심 키워드**: MLP, Activation(ReLU, Sigmoid), Regularization(Dropout, Weight Decay), Batch Normalization, Class Imbalance, pos_weight
- **주요 실습**: 
    - **Boston Housing**: 회귀 모델 고도화
    - **Titanic Survival**: 이진 분류 기초 및 성능 지표
    - **Employee Attrition**: 불균형 데이터 대응
    - **MNIST Intro**: 이미지 전처리 및 다중 분류 기초

### 🔵 Theme 18: 합성곱 신경망(CNN) 및 이미지 분류 (2026-05-12)
이미지 데이터의 공간적 구조를 보존하며 효율적으로 특징을 추출하는 CNN의 구조와 원리를 학습합니다.

- **핵심 키워드**: Convolution Layer, Pooling Layer, Padding, Stride, Channel, Filter(Kernel), Feature Map, Flatten
- **주요 실습**:
    - **MNIST with CNN**: MLP와 CNN의 성능 비교 및 파라미터 효율성 검증
    - **CIFAR-10**: 컬러 이미지 처리 및 데이터 증강(Augmentation) 기법 적용
    - **CNN 구조 설계**: 고유의 CNN 아키텍처 구현 및 레이어별 피처맵 시각화

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-11.ipynb](05-11.ipynb): 보스턴/타이타닉/이직예측 딥러닝 실습 전체 과정 (완료)
- [05-12.ipynb](05-12.ipynb): CNN 기초 및 MNIST 이미지 분류 실습 (완료)
- **트러블슈팅 리포트**:
    - [2026-05-11 리포트](./troubleshooting/2026-05-11.md): 과적합 제어 전략 및 불균형 데이터 해결 리포트
    - [2026-05-12 리포트](./troubleshooting/2026-05-12.md): CNN 차원 계산 및 ROI 종횡비 왜곡 해결 리포트 (완료)

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `PyTorch`, `Scikit-Learn`, `Pandas`, `NumPy`, `OpenCV`
- **Architecture**: Multi-Layer Perceptron (MLP), Convolutional Neural Networks (CNN)
