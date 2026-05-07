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

### 🟢 Theme 15: 비지도학습 기반 군집화(Clustering) 및 성능 평가 (2026-05-07)
데이터의 정답 없이 유사한 특성을 가진 그룹을 식별하고, 실루엣 계수를 통해 군집의 품질을 정량적으로 평가했습니다.
- **핵심 키워드**: KMeans, GMM, Inertia, Elbow Method, Silhouette Score, Yellowbrick
- **주요 실습**:
    - **KMeans**: 거리 기반 군집화 및 Elbow Method를 통한 최적 K(3) 도출
    - **GMM**: 확률 분포 기반 군집화 및 KMeans와의 특성 비교 (실루엣 점수 비교: KMeans 0.55 > GMM 0.50)
    - **성능 평가**: Yellowbrick `SilhouetteVisualizer`를 활용한 군집별 응집도 시각화 및 검증

---

## 💻 주요 폴더 및 소스 코드 구조

### 📓 실습 노트북 및 리포트
- [05-06.ipynb](05-06.ipynb): 센서 데이터 분석 및 모델링 전체 과정 (실습 완료)
- [05-07.ipynb](05-07.ipynb): 차원 축소 알고리즘(PCA, LDA, SVD) 비교 실습 (진행 중)
- **트러블슈팅 리포트**:
    - [2026-05-06 리포트](./troubleshooting/2026-05-06.md): CRISP-DM 요약 및 XGBoost 라벨 인코딩 이슈 해결.
    - [2026-05-07 리포트](./troubleshooting/2026-05-07.md): 차원 축소 알고리즘 선택 기준 및 PCA vs SVD 상관관계 분석.

---

## 🛠️ 사용 기술 및 의존성
- **Libraries**: `Pandas`, `NumPy`, `Scikit-Learn` 등
