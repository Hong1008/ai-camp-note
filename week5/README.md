# Week 5: 머신러닝 기초 및 회귀 모델 (Machine Learning Basics)

5주차에는 데이터 분석(EDA)을 넘어, 데이터를 활용해 미래를 예측하는 **머신러닝(Machine Learning)**의 기초를 학습합니다. 데이터 전처리부터 회귀 모델의 성능 평가까지 실습을 진행합니다.

---

## 🗓️ 학습 로드맵

### 🟡 Theme 8: 머신러닝 기초 및 회귀 모델 (2026-04-24)
머신러닝의 기본 개념을 이해하고, 수치 데이터를 예측하는 선형 회귀 모델의 전체 프로세스를 실습했습니다.
- **개념 학습**: 머신러닝과 모델링의 정의, 전통적 프로그래밍과의 차이점 이해.
- **데이터 전처리**: `train_test_split`을 활용한 데이터 분할(Train/Test)의 중요성과 데이터 누수(Leakage) 방지 전략 학습.
- **모델링 실습**: `scikit-learn` 라이브러리를 활용한 `LinearRegression` 모델 구축 및 `fit`을 통한 학습 수행.
- **성능 평가**: `MAE(Mean Absolute Error)` 지표를 통해 모델의 예측 오차를 정량적으로 해석하는 방법 습득.

### 🟢 Theme 9: 단순 및 다중 회귀 모델 (Regression)
수치형 타겟을 예측하는 모델을 구축하고 평가합니다.
- **선형 회귀 (Linear Regression)**: 최소제곱법(OLS)의 원리 이해.
- **성능 평가 지표**: MSE, RMSE, MAE, R-Squared($R^2$)의 의미와 해석.
- **변수 선택**: 상관관계와 모델 성능 사이의 균형 잡기.

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [04-24.ipynb](04-24.ipynb): 머신러닝 데이터 전처리 및 회귀 기초 실습.
- **트러블슈팅 리포트**:
    - [2026-04-24 리포트](./troubleshooting/2026-04-24.md): 데이터 누수(Data Leakage) 및 스케일링 이슈 대응.

---

## 🛠️ 사용 기술 및 의존성
- **Machine Learning**: `Scikit-Learn`
- **Data Analysis**: `Pandas`, `NumPy`
- **Visualization**: `Matplotlib`, `Seaborn`
