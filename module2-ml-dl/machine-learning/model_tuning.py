"""모델 성능 개선 (과대적합 규제 · 교차검증 · GridSearchCV) - 2026-10-19 TIL, 개념 정리는 README.md 참고"""

import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score

# 데이터 불러오기
file_path = "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
df = pd.read_csv(file_path)
print(df)

print("-" * 80)

# 학습용과 평가용 데이터 생성 (80:20)
X_data = df.drop(columns=["Diabetes_binary"])
y_data = df["Diabetes_binary"]

X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

print(f"X_train 행 인덱스: \n{X_train.index}")
print(f"y_train 행 인덱스: \n{y_train.index}")

ratio_train = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답 항목별 비율: \n{ratio_train}")

print("-" * 80)

# 1. max_depth 직접 지정한 결정 트리
dt = DecisionTreeClassifier(max_depth=9, random_state=0)
dt.fit(X_train, y_train)

print(f"학습된 모델의 최대 깊이: {dt.get_depth()}")

plt.figure(figsize=(15, 10))
plot_tree(decision_tree=dt, feature_names=X_train.columns, max_depth=3)
plt.show()

pred_test_dt = dt.predict(X_test)
accuracy_dt = accuracy_score(y_test, pred_test_dt)
print(f"max_depth=9 결정 트리의 평가용 데이터 성능: {accuracy_dt:.4f}")

print("-" * 80)

# 2. GridSearchCV를 이용한 결정 트리 고도화
dt_base = DecisionTreeClassifier(random_state=0)

params = {
    "max_depth": [3, 4, 5, 6, 7, 8, 9, 10],
    "min_samples_leaf": [2, 3, 4, 5]
}

grid_dt = GridSearchCV(
    estimator=dt_base,
    param_grid=params,
    scoring="accuracy",
    cv=5
)

grid_dt.fit(X_train, y_train)
print("탐색 완료")

best_dt = grid_dt.best_estimator_
print(f"최적의 하이퍼파라미터: {grid_dt.best_params_}")
print(f"최적 모델: {best_dt}")
print(f"교차검증 최고 점수: {grid_dt.best_score_:.4f}")

pred_test_best = best_dt.predict(X_test)
acc_best = accuracy_score(y_test, pred_test_best)
print(f"고도화된 DecisionTree 분류 모델의 평가용 데이터 성능: {acc_best:.4f}")

# RandomForest 분류 모델 고도화

## GridSearchCV 탐색 도구를 이용한 고도화

### 필요한 클래스 임포트
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

### 성능 고도화 대상 모델 생성
rf = RandomForestClassifier(random_state=0)

### 최적화 할 매개 변수와 탐색 조건 설정 -> 4 * 5 * 4 = 80가지 조합
params = {
    "n_estimators": [100, 200, 300, 400],
    "max_depth": [5, 6, 7, 8, 9],
    "min_samples_leaf": [2, 3, 4, 5]
}

### 탐색 도구 생성
grid_rf = GridSearchCV(
    estimator=rf,
    param_grid=params,
    scoring="accuracy",
    cv=5
)

### 탐색 도구 학습 및 검증
grid_rf.fit(X_train, y_train)
print("탐색 완료")

### best 모델 추출
best_rf = grid_rf.best_estimator_
print(best_rf)

### 검증용 데이터에 대한 최적의 성능
print(grid_rf.best_score_)

## 평가용 데이터를 이용한 예측
pred_test_rf = best_rf.predict(X_test)

## 모델 평가 -> classification_report로 4가지 성능 측정
from sklearn.metrics import classification_report

performance_rf = classification_report(y_test, pred_test_rf)
print(f"고도화된 RandomForest 분류 모델의 평가용 데이터에 대한 4가지 성능: \n{performance_rf}")

# RandomizedSearchCV 탐색 도구를 이용한 RandomForest 분류 모델 고도화

## 필요한 클래스 임포트
from sklearn.model_selection import RandomizedSearchCV

## 성능 고도화 대상 모델 생성
rf = RandomForestClassifier(random_state=0)

## 최적화 할 매개 변수와 탐색 조건 설정 -> 10 * 6 * 4 = 240가지 조합
params = {
    "n_estimators": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    "max_depth": [5, 6, 7, 8, 9, 10],
    "min_samples_leaf": [2, 3, 4, 5]
}

## 탐색 도구 생성
### n_iter: 전체 240가지 중 무작위로 추출해서 탐색할 횟수
random_rf = RandomizedSearchCV(
    estimator=rf,
    param_distributions=params,
    n_iter=30,
    scoring="f1",
    cv=5,
    random_state=0
)

## 탐색 도구 학습 및 검증
random_rf.fit(X_train, y_train)
print("학습 완료")

## best 모델 추출
best_rf_random = random_rf.best_estimator_
print(best_rf_random)

## 검증용 데이터에 대한 최적의 성능 확인
print(random_rf.best_score_)

## 평가용 데이터를 이용한 예측 및 평가
pred_test_rf_random = best_rf_random.predict(X_test)
performance_rf_random = classification_report(y_test, pred_test_rf_random)
print(f"평가용 데이터에 대한 4가지 성능: \n{performance_rf_random}")

# XGBoost 분류 모델 고도화

## 필요한 클래스 임포트
from xgboost import XGBClassifier

## 성능 고도화 대상 모델 생성
xgb = XGBClassifier(random_state=0)

## 최적화 할 매개 변수와 탐색 범위 설정
### learning_rate: 새 트리가 오차를 보정하는 값을 한 번에 얼마나 반영할지(보폭)
### 부스팅 -> 모델의 오차 감소량 * learning_rate = 실제 적용되는 오차 감소량
params = {
    "n_estimators": [50, 100, 200, 300],
    "learning_rate": [0.05, 0.1, 0.5],
    "max_depth": [3, 4, 5]
}

## 탐색 도구 생성
grid_xgb = GridSearchCV(
    estimator=xgb,
    param_grid=params,
    scoring="f1",
    cv=5
)

## 탐색 도구 학습 및 검증
grid_xgb.fit(X_train, y_train)
print("검증 완료")

## best 모델 추출
best_xgb = grid_xgb.best_estimator_
print(best_xgb)

## 검증용 데이터에 대한 최적의 성능 확인
print(grid_xgb.best_score_)

## 평가용 데이터를 이용한 예측 및 평가
pred_test_xgb = best_xgb.predict(X_test)
performance_xgb = classification_report(y_test, pred_test_xgb)
print(f"고도화된 XGBoost 분류 모델의 평가용 데이터에 대한 4가지 성능: \n{performance_xgb}")

# Stacking 분류 모델

## 1단계: 개별 기본 모델 생성
### 앞에서 고도화를 완료한 개별 모델을 Stacking의 기본 모델로 지정
base_models = [
    ("dt", best_dt),
    ("rf", best_rf),
    ("xgb", best_xgb)
]

## 2단계: 최종 메타 모델 생성
### 1단계 모델들의 예측값을 받아 최종 판단을 내리는 모델
from sklearn.linear_model import LogisticRegression

final_meta = LogisticRegression(max_iter=1000)

## Stacking 모델 생성 -> base_models와 final_meta 결합
from sklearn.ensemble import StackingClassifier

stack = StackingClassifier(
    estimators=base_models,
    final_estimator=final_meta
)

## 모델 학습
stack.fit(X_train, y_train)
print("학습 완료")

## 평가용 데이터에 대한 예측 및 평가
pred_test_stack = stack.predict(X_test)
performance_stack = classification_report(y_test, pred_test_stack)
print(f"Stacking 분류 모델의 평가용 데이터에 대한 4가지 성능: \n{performance_stack}")

# best 모델 저장 및 재사용

## 필요한 라이브러리 임포트
import joblib

## best 모델 저장 -> 확장자 .pkl(pickle)
joblib.dump(best_rf_random, "best_rf_random.pkl")

## best 모델 불러오기 -> 학습이 완료된 상태 그대로 복원
loaded_best_rf_random = joblib.load("best_rf_random.pkl")
print(loaded_best_rf_random)

## 불러온 모델을 이용한 성능 측정

### 평가용 데이터를 이용한 예측
pred_test_rf_random_loaded = loaded_best_rf_random.predict(X_test)

### 평가용 데이터를 이용한 성능 평가
performance_rf_random_loaded = classification_report(y_test, pred_test_rf_random_loaded)

### 결과 확인 -> 저장 전과 동일한 성능이 나오는지 확인
print(f"불러온 모델을 이용한 평가용 데이터에 대한 4가지 성능: \n{performance_rf_random_loaded}")
