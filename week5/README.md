# Week 5: 머신러닝 기초 및 모델링 (Machine Learning Basics)

5주차에는 데이터 분석(EDA)을 넘어, 데이터를 활용해 미래를 예측하는 **머신러닝(Machine Learning)**의 기초를 학습합니다. 데이터 전처리부터 회귀 및 분류 모델의 구축, 그리고 성능 평가까지의 전 과정을 실습합니다.

---

## 🗓️ 학습 로드맵

### 🟡 Theme 8: 머신러닝 기초 및 회귀 모델 기초 (2026-04-24)
머신러닝의 기본 개념을 이해하고, 선형 회귀 모델의 전체 프로세스를 학습했습니다.
- **데이터 전처리**: `train_test_split`을 활용한 데이터 분할 및 누수 방지 전략.
- **모델링 실습**: `LinearRegression` 모델 구축 및 `fit` 학습 수행.
- **성능 평가**: `MAE` 지표를 활용한 오차 해석 기초.

### 🟢 Theme 9: 회귀 및 분류 모델 심화 (2026-04-27)
수치 예측(회귀)과 범주 예측(분류)의 차이를 이해하고 다양한 알고리즘을 실습했습니다.

#### 1. 회귀 모델 (Regression)
- **단순 vs 다중 회귀**: 독립 변수 개수에 따른 수식 구성 및 시각화 기법의 차이.
- **평가 지표**: MSE, RMSE, MAE, $R^2$의 수학적 의미와 상황별 선택 기준.
- **변수 선택**: 상관관계 분석 및 다중공선성(Multicollinearity) 예방 전략.

#### 2. 분류 모델 (Classification)
- **주요 알고리즘**:
    - **KNN (K-Nearest Neighbors)**: 거리 기반 유유상종 원리 및 스케일링의 중요성.
    - **Decision Tree**: 스무고개 기반 규칙 생성 및 `max_depth`를 통한 과적합 제어.
- **성능 평가**: 혼동 행렬(Confusion Matrix) 기반의 Accuracy, Precision, Recall, F1-Score 이해.

### 🟠 Theme 10: 분류 모델 심화 및 성능 최적화 (2026-04-28)
다양한 분류 알고리즘(KNN, Decision Tree, SVM)의 하이퍼파라미터 튜닝과 불균형 데이터 대응 전략을 실습했습니다.
- **하이퍼파라미터 튜닝**: KNN의 최적 K값 탐색 및 결정 트리의 `max_depth` 시각화 분석.
- **SVM (Support Vector Machine)**: 마진 최대화 원리 및 커널 트릭(RBF, Linear)의 이해.
- **불균형 데이터 대응**: 정확도의 함정(Accuracy Paradox) 이해 및 임계값(Threshold) 조정을 통한 재현율(Recall) 최적화.
- **모델 시각화**: `plot_tree`를 활용한 의사결정 로직 해석 및 SVR의 엡실론 튜브 시각화.
### 🔵 Theme 11: 교차 검증 및 로지스틱 회귀 (2026-04-29) [COMPLETED]
모델의 일반화 성능을 극대화하기 위한 검증 전략과 확률 기반 분류 모델인 로지스틱 회귀를 학습했습니다.
- **교차 검증 (Cross Validation)**: `K-Fold`의 원리와 데이터 낭비 없는 성능 평가 기법. 데이터 규모에 따른 표준편차(안정성) 해석.
- **로지스틱 회귀 (Logistic Regression)**: 시그모이드 함수를 활용한 확률 도출 및 선형 회귀와의 차이점 이해.
- **하이퍼파라미터 최적화**: `GridSearchCV`와 `RandomizedSearchCV`의 차이점 및 하이브리드 튜닝 전략.
- **심화 지표**: `ROC Curve`와 `AUC`를 활용한 불균형 데이터 구별 능력 평가.
- **SVR 실습**: 회귀용 SVM인 `SVR` 적용 및 거리 기반 모델에서 스케일링의 결정적 역할 확인.


---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [04-24.ipynb](04-24.ipynb): 머신러닝 데이터 전처리 및 회귀 기초 실습.
- [04-27.ipynb](04-27.ipynb): 단순/다중 회귀 및 분류(KNN, Decision Tree) 모델링 실습.
- [04-28.ipynb](04-28.ipynb): 분류 모델 심화(SVM 포함) 및 임계값 조정, 시각화 실습.
- [04-29.ipynb](04-29.ipynb): 교차 검증(K-Fold) 및 로지스틱 회귀 모델링 실습.
- **트러블슈팅 리포트**:
    - [2026-04-24 리포트](./troubleshooting/2026-04-24.md): 데이터 누수 및 스케일링 이슈 대응.
    - [2026-04-27 리포트](./troubleshooting/2026-04-27.md): 인덱스 불일치, 다중공선성, 모델별 시각화 한계점 대응.
    - [2026-04-28 리포트](./troubleshooting/2026-04-28.md): 평가 지표 길이 불일치, 시각화 타입 에러 및 불균형 데이터 튜닝 리포트.
    - [2026-04-29 리포트](./troubleshooting/2026-04-29.md): 교차 검증 시 데이터 분할 이슈 및 로지스틱 회귀 해석 리포트.

---

## 🛠️ 사용 기술 및 의존성
- **Machine Learning**: `Scikit-Learn` (`LinearRegression`, `KNeighborsClassifier`, `DecisionTreeClassifier`, `SVC`, `SVR`, `LogisticRegression`, `KFold`, `cross_val_score`)
- **Data Analysis**: `Pandas`, `NumPy`
- **Visualization**: `Matplotlib`, `Seaborn`, `plot_tree`
