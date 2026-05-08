# Week 6: Human Activity Recognition & Model Optimization

6주차 학습을 시작합니다. 이번 주차에는 **머신러닝 모델의 해석(Explainability)과 최적화(Optimization)**를 중점적으로 다룹니다.

---

## 🗓️ 학습 로드맵

### 🟡 Theme 13: 센서 데이터 분석 및 XGBoost 최적화 (2026-05-06)
CRISP-DM 프로세스에 따라 센서 데이터를 분석하고, 최첨단 분류 모델인 XGBoost를 구축 및 튜닝했습니다.
- **핵심 키워드**: CRISP-DM, Feature Importance, XGBoost, Label Encoding, Optuna, joblib
- **주요 실습**: 
    - 561개 센서 피처 분석 및 상위 95개 핵심 변수 선별
    - Optuna를 이용한 XGBoost 하이퍼파라미터 자동 최적화 실습
    - CRISP-DM 기반 분석 파이프라인 구축 및 모델 저장

### 🔵 Theme 14: 차원 축소(Dimension Reduction) 기법 비교 분석 (2026-05-07)
고차원 데이터의 정보를 보존하면서 효율적으로 압축하는 다양한 차원 축소 알고리즘의 원리를 이해하고 성능을 비교했습니다.
- **핵심 키워드**: PCA, LDA, TruncatedSVD, Standardization, Explained Variance Ratio
- **주요 실습**:
    - **PCA**: 비지도학습 기반 분산 최대화 축소 (Iris 정확도 88%, 신용카드 데이터 중복성 제거)
    - **LDA**: 지도학습 기반 클래스 분별력 최대화 축소 (Iris 정확도 95.3%로 최우수)
    - **TruncatedSVD**: 희소 행렬 처리에 강점이 있는 기법 (Center화 데이터에서 PCA와 동일 성능 확인)

### 🟣 Theme 16: RFM 고객 세분화 및 딥러닝 기초 (2026-05-08)
데이터 전처리와 비지도 학습의 결합, 그리고 인공신경망의 기본 원리를 이해하고 실제 모델로 구현했습니다.
- **핵심 키워드**: RFM Analysis, Log Transformation, Perceptron, Backpropagation, Adam Optimizer, PyTorch, Overfitting, Dropout
- **주요 실습**:
    - **RFM 고도화**: 로그 변환(`log1p`)을 통한 이상치 제어 및 계층적 군집화(Tiered Clustering) 전략 수립
    - **Deep Learning 구현**: 
        - Numpy를 이용한 퍼셉트론 및 학습 루프 바닥부터 구현하기
        - PyTorch를 활용한 보스턴 집값 예측 모델 구축 및 성능 최적화 (38.6 ➜ 7.25 Loss 개선)
        - 과적합(Overfitting) 진단 및 규제(Dropout, Weight Decay) 적용

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-06.ipynb](05-06.ipynb): 센서 데이터 분석 및 모델링 전체 과정 (실습 완료)
- [05-07.ipynb](05-07.ipynb): 차원 축소 알고리즘(PCA, LDA, SVD) 비교 및 군집화 기초 (실습 완료)
- [05-08.ipynb](05-08.ipynb): RFM 세분화 고도화 및 딥러닝 입문 실습 (진행 중)
- **트러블슈팅 리포트**:
    - [2026-05-06 리포트](./troubleshooting/2026-05-06.md): CRISP-DM 요약 및 XGBoost 라벨 인코딩 이슈 해결.
    - [2026-05-07 리포트](./troubleshooting/2026-05-07.md): 차원 축소 알고리즘 선택 기준 및 PCA vs SVD 상관관계 분석.
    - [2026-05-08 리포트](./troubleshooting/2026-05-08.md): RFM 시각화 매핑 오류 해결 및 딥러닝 과적합 제어 전략.

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `Pandas`, `NumPy`, `Scikit-Learn` 등
