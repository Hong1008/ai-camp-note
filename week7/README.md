# Week 7: Deep Learning Foundations & Neural Networks

7주차 학습을 시작합니다. 이번 주차에는 **딥러닝의 기초 원리와 신경망 모델의 설계 및 학습**을 중점적으로 다룹니다.

---

## 🗓️ 학습 로드맵

### 🟡 Theme 17: 신경망의 원리 및 PyTorch 심화 (2026-05-11)
인공 신경망의 수학적 구조와 역전파(Backpropagation) 알고리즘을 이해하고, 다양한 데이터셋에 최적화된 모델링을 실습했습니다.

- **핵심 키워드**: MLP, Activation(ReLU, Sigmoid), Regularization(Dropout, Weight Decay), Batch Normalization, Class Imbalance, pos_weight
- **주요 실습**: 
    - **Boston Housing**: 회귀 모델 고도화 (MAPE 42% ➜ 4.5% 개선)
    - **Titanic Survival**: 이진 분류 기초 및 분류 평가지표(F1-score, Confusion Matrix) 학습
    - **Employee Attrition**: 불균형 데이터 대응 및 Recall 성능 최적화
    - **MNIST Intro**: 이미지 데이터 전처리(Normalization, Reshaping) 및 다중 분류 기초

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-11.ipynb](05-11.ipynb): 보스턴/타이타닉/이직예측 딥러닝 실습 전체 과정 (완료)
- **트러블슈팅 리포트**:
    - [2026-05-11 리포트](./troubleshooting/2026-05-11.md): 과적합 제어 전략 및 불균형 데이터 해결 리포트

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `PyTorch`, `Scikit-Learn`, `Pandas`, `NumPy`
- **Architecture**: Multi-Layer Perceptron (MLP)
