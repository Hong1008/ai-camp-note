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

### 🔴 Theme 19: CNN 심화 및 컬러 이미지 분류 (2026-05-13)
컬러 이미지 데이터셋(CIFAR-10)을 활용하여 더 깊은 네트워크를 설계하고, 과적합을 방지하기 위한 정규화 및 증강 기법을 학습합니다.

- **핵심 키워드**: RGB Color Channels, Data Augmentation, Dropout, Batch Normalization, Global Average Pooling
- **주요 실습**:
    - **CIFAR-10 Classification**: 컬러 이미지 특화 CNN 설계
    - **Performance Tuning**: Dropout 및 BN 적용 전후 성능 비교
    - **Augmentation Pipeline**: `torchvision.transforms`를 이용한 실시간 증강

### 🔵 Theme 20: 전이 학습(Transfer Learning) 및 실무 모델 활용 (2026-05-14)
거대 데이터셋으로 학습된 모델을 목적에 맞게 재사용하는 전이 학습 기법을 배우고, 실무 수준의 이미지 분류 성능을 달성합니다.

- **핵심 키워드**: Transfer Learning, Feature Extraction, Fine-Tuning, Pre-trained Model (ResNet, VGG), Weights
- **주요 실습**:
    - **ResNet-18 Transfer**: 사전 학습 모델 로드 및 Classifier 수정
    - **Freezing Strategy**: `requires_grad`를 이용한 학습 범위 조절
    - **ImageNet Stats**: 모델에 특화된 정규화 및 전처리 적용

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-11.ipynb](05-11.ipynb): 보스턴/타이타닉/이직예측 딥러닝 실습 전체 과정 (완료)
- [05-12.ipynb](05-12.ipynb): CNN 기초 및 MNIST 이미지 분류 실습 (완료)
- [05-13.ipynb](05-13.ipynb): CIFAR-10 컬러 이미지 분류 및 성능 고도화 (완료)
- [05-14.ipynb](05-14.ipynb): 전이 학습 및 사전 학습 모델 활용 실습 (진행 중)
- **트러블슈팅 리포트**:
    - [2026-05-11 리포트](./troubleshooting/2026-05-11.md): 과적합 제어 전략 및 불균형 데이터 해결 리포트
    - [2026-05-12 리포트](./troubleshooting/2026-05-12.md): CNN 차원 계산 및 ROI 종횡비 왜곡 해결 리포트 (완료)
    - [2026-05-13 리포트](./troubleshooting/2026-05-13.md): CIFAR-10 전처리 및 Augmentation 전략 리포트 (완료)
    - [2026-05-14 리포트](./troubleshooting/2026-05-14.md): 전이 학습 전략 및 모델 튜닝 리포트 (진행 중)

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `PyTorch`, `Scikit-Learn`, `Pandas`, `NumPy`, `OpenCV`
- **Architecture**: Multi-Layer Perceptron (MLP), Convolutional Neural Networks (CNN), Transfer Learning (ResNet)
