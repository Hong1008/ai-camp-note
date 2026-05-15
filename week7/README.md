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

### 🟣 [x] Theme 21: 실전 딥러닝 파이프라인 및 모델 서빙 (2026-05-15)
7주차를 마무리하며, 전이 학습 모델의 성능을 극대화하기 위한 스케줄링 기법과 학습된 모델을 저장/로드하여 실제 추론에 활용하는 파이프라인을 구축합니다.

- **핵심 키워드**: Learning Rate Scheduler (Cosine Annealing), Early Stopping, Model Save/Load, Inference Pipeline, TTA (Test Time Augmentation)
- **주요 실습**:
    - **Advanced Optimization**: Scheduler 및 Early Stopping 적용 실습
    - **Inference System**: 단일 이미지 입력에 대한 모델 예측 및 결과 가시화
    - **Final Project**: CIFAR-10 고성능 분류기 완성 및 저장

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-11.ipynb](05-11.ipynb): 보스턴/타이타닉/이직예측 딥러닝 실습 전체 과정 (완료)
- [05-12.ipynb](05-12.ipynb): CNN 기초 및 MNIST 이미지 분류 실습 (완료)
- [05-13.ipynb](05-13.ipynb): CIFAR-10 컬러 이미지 분류 및 성능 고도화 (완료)
- [05-14.ipynb](05-14.ipynb): 전이 학습 및 사전 학습 모델 활용 실습 (완료)
- [05-15.ipynb](05-15.ipynb): 실전 딥러닝 파이프라인 및 모델 서빙 (완료)
- **트러블슈팅 리포트**:
    - [2026-05-11 리포트](./troubleshooting/2026-05-11.md): 과적합 제어 전략 및 불균형 데이터 해결 리포트
    - [2026-05-12 리포트](./troubleshooting/2026-05-12.md): CNN 차원 계산 및 ROI 종횡비 왜곡 해결 리포트 (완료)
    - [2026-05-13 리포트](./troubleshooting/2026-05-13.md): CIFAR-10 전처리 및 Augmentation 전략 리포트 (완료)
    - [2026-05-14 리포트](./troubleshooting/2026-05-14.md): 전이 학습 전략 및 모델 튜닝 리포트 (완료)
    - [2026-05-15 리포트](./troubleshooting/2026-05-15.md): 모델 서빙 및 성능 고도화 리포트 (완료)

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `PyTorch`, `Scikit-Learn`, `Pandas`, `NumPy`, `OpenCV`
- **Architecture**: Multi-Layer Perceptron (MLP), Convolutional Neural Networks (CNN), Transfer Learning (ResNet)
- **Advanced**: Cosine Annealing LR, Early Stopping, Serialization
