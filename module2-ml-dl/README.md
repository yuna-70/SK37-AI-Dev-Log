# Module 2 - 데이터 분석과 머신러닝/딥러닝

> 2026년 9월 29일 시작

## 📚 학습 내용

**데이터 분석**
- NumPy: array 생성, 차원과 shape, 인덱싱, 슬라이싱
- pandas: Series / DataFrame / Index, `read_csv()`, 파생 변수 생성
- 데이터 전처리: 결측치 처리, `groupby()` + `agg()`, 이상치(IQR) 처리
- 데이터 탐색: 상관관계 분석, EDA
- 시각화: matplotlib, seaborn, plotly

**머신러닝**
- 기본 개념: 지도 / 비지도 학습, Train/Test Split, 평가 척도
- 데이터 전처리: One-Hot / Label 인코딩, 표준화·정규화, 구간화(`pd.cut`)
- 회귀: 선형 회귀, 다중 선형 회귀, MAE / MSE / RMSE
- 모델 정규화: L1 규제(Lasso), L2 규제(Ridge)
- 분류: 로지스틱 회귀와 시그모이드, SVM, 결정 트리
- 앙상블: Voting, 베깅·페이스팅, 랜덤 포레스트, 부스팅(XGBoost), 스태킹
- 비지도 학습: 차원 축소(PCA), K-Means 군집화, AutoML(AutoGluon)
- 모델 검증: K-fold 교차검증, GridSearchCV, RandomizedSearchCV, `joblib`
- 모델 평가: Confusion Matrix, 정밀도 / 재현율 / F1-score
- 특성 중요도: `feature_importances_`, 순열 특성 중요도

**딥러닝**
- 퍼셉트론: 가중치와 편향, 논리 게이트, XOR 난제와 다층 퍼셉트론
- 활성화 함수: 계단, 시그모이드, ReLU, 소프트맥스
- 손실 함수: MSE, 교차 엔트로피 오차(CEE), BCE
- 학습 원리: 수치 미분, 편미분과 기울기, 경사하강법
- 오차역전파: 계산 그래프, 연쇄법칙
- 최적화 알고리즘: SGD, 모멘텀, AdaGrad, Adam
- PyTorch: Tensor, TensorDataset / DataLoader, `nn.Linear`, `nn.Sequential`
- MLP 구현: 이진 분류(타이타닉), 회귀(보스턴 주택 가격)

## 📖 훈련 교재

- 파이썬 머신러닝 판다스 데이터 분석
- 파이토치 딥러닝 마스터

## 🚀 프로젝트

가입 고객 이탈 예측

## 📂 폴더 구조

- `data-analysis/` — NumPy, pandas, 데이터 전처리, EDA, 시각화
- `machine-learning/` — 전처리, 회귀·분류, 앙상블, 모델 검증 및 평가
- `deep-learning/` — 퍼셉트론, 활성화 함수, 오차역전파, 최적화, PyTorch MLP