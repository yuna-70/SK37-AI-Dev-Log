"""TIL: 순열 특성 중요도와 DecisionTree 고도화 - Telco 고객 이탈 (2026-10-27) — 개념 설명은 README.md 참고"""

# 파이썬 경고 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 데이터 불러오기 및 전처리
### 전처리·EDA 과정은 machine-learning/telco_churn.py와 동일하므로 요약만 작성

## 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
import plotly.express as px

## DataFrame 생성
file_path = "Telco-Customer-Churn.csv"
df = pd.read_csv(file_path)

## TotalCharges 컬럼: 공백 문자열을 누락으로 변환 후 해당 행 제거
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df1 = df.dropna(ignore_index=True)

## 불필요한 컬럼 제거 및 인코딩
df2 = df1.drop(columns=["customerID"])
df2["Churn"] = df2["Churn"].map({"No": 0, "Yes": 1})

categorical_cols_list = df2.select_dtypes(include=["object"]).columns.tolist()
df_onehot = pd.get_dummies(data=df2, columns=categorical_cols_list, dtype=int)

# 학습용과 평가용 데이터 생성

## 필요한 함수 임포트
from sklearn.model_selection import train_test_split

X_data = df_onehot.drop(columns=["Churn"])
y_data = df_onehot["Churn"]

## 80:20의 비율로 분할 -> 무작위성 통제 -> random_state, stratify
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터의 정답 비율 확인 -> stratify 적용 여부 확인
ratio_train = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답의 항목별 비율: \n{ratio_train}")

# LogisticRegression 분류 모델 고도화

## 필요한 클래스 임포트
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report

## 성능 고도화 대상 모델 생성
lr = LogisticRegression(random_state=0)

## 최적화 할 매개 변수와 탐색의 조건 설정 -> 5 * 4 = 20가지
params = {
    "C": [0.01, 0.1, 1, 10, 100],
    "max_iter": [100, 500, 1000, 5000]
}

## 탐색 도구 생성 및 학습
grid_lr = GridSearchCV(
    estimator=lr,
    param_grid=params,
    scoring="f1",
    cv=5
)
grid_lr.fit(X_train, y_train)
print("검증 완료")

## best 모델 추출
best_lr = grid_lr.best_estimator_
print(best_lr)
print(grid_lr.best_score_)

## 평가용 데이터를 이용한 예측 및 평가
pred_test_best_lr = best_lr.predict(X_test)

performance_best_lr = classification_report(y_test, pred_test_best_lr)
print(f"고도화된 LogisticRegression 모델의 4가지 성능: \n{performance_best_lr}")

# LogisticRegression: 평가용 데이터에 대한 순열 특성 중요도

## 필요한 함수 임포트
from sklearn.inspection import permutation_importance

## 평가용 데이터에서 특정 컬럼을 무작위로 섞었을 때의 성능(f1) 감소량 측정
### n_repeats: 섞는 횟수 -> 여러 번 섞어 평균을 내야 우연을 배제할 수 있음
lr_perm_result = permutation_importance(
    estimator=best_lr,
    X=X_test,
    y=y_test,
    scoring="f1",
    n_repeats=5,
    random_state=0
)

## 특성의 중요도와 컬럼 이름 -> dict 자료형 생성
### importances_mean: n_repeats번 측정한 성능 감소량의 평균
data_dict_test = {
    "Feature": X_train.columns,
    "Importance_mean": lr_perm_result.importances_mean
}

## DataFrame 생성 및 내림차순 정렬
df_best_lr_test_imp = pd.DataFrame(data=data_dict_test).sort_values(by="Importance_mean", ascending=False)
display(df_best_lr_test_imp)

## 상위 5개 추출 및 시각화
df_best_lr_test_imp_top5 = df_best_lr_test_imp.head(5)

fig1 = px.bar(
    data_frame=df_best_lr_test_imp_top5,
    x="Feature",
    y="Importance_mean",
    text_auto=".4f",
    title="[LogisticRegression] 평가용 데이터 특성 중요도 Top5"
)
fig1.show()

# DecisionTree 분류 모델 고도화

## 필요한 클래스 임포트
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV

## 성능 고도화 대상 모델 생성
dt = DecisionTreeClassifier(random_state=0)

## 최적화 할 매개 변수와 탐색의 조건 설정 -> 28 * 19 = 532가지
params = {
    "max_depth": range(3, 31),
    "min_samples_leaf": range(2, 21)
}

## 탐색 도구 생성 -> 532가지 중 150가지만 무작위로 탐색
random_dt = RandomizedSearchCV(
    estimator=dt,
    param_distributions=params,
    n_iter=150,
    scoring="f1",
    cv=5,
    random_state=0
)

## 탐색 도구 학습 및 검증
random_dt.fit(X_train, y_train)
print("검증 완료")

## best 모델 추출
best_dt = random_dt.best_estimator_
print(best_dt)
print(random_dt.best_score_)

# DecisionTree: 학습용 데이터에 대한 내장 특성 중요도

## 결정 트리 계열은 feature_importances_를 제공함(불순도 감소량 기준)
dt_train_importances = best_dt.feature_importances_

data_dict_train = {
    "Feature": X_train.columns,
    "Importance": dt_train_importances
}

df_dt_train_importances = pd.DataFrame(data=data_dict_train).sort_values(by="Importance", ascending=False)

## 상위 10개 추출 및 시각화
top10_dt_train_importances = df_dt_train_importances.head(10)

fig2 = px.bar(
    data_frame=top10_dt_train_importances,
    x="Feature",
    y="Importance",
    title="[DecisionTree 분류 모델] 학습용 데이터에 대한 특성 중요도 Top10"
)
fig2.show()

## 평가용 데이터를 이용한 예측 및 평가
pred_test_dt = best_dt.predict(X_test)

performance_dt = classification_report(y_test, pred_test_dt)
print(f"고도화된 DecisionTree 분류 모델의 성능: \n{performance_dt}")

# DecisionTree: 평가용 데이터에 대한 순열 특성 중요도

dt_perm_result = permutation_importance(
    estimator=best_dt,
    X=X_test,
    y=y_test,
    scoring="f1",
    n_repeats=5,
    random_state=0
)

data_dict_test = {
    "Feature": X_train.columns,
    "Importance_mean": dt_perm_result.importances_mean
}

df_best_dt_test_imp = pd.DataFrame(data=data_dict_test).sort_values(by="Importance_mean", ascending=False)

## 상위 5개 추출 및 시각화
df_best_dt_test_imp_top5 = df_best_dt_test_imp.head(5)

fig3 = px.bar(
    data_frame=df_best_dt_test_imp_top5,
    x="Feature",
    y="Importance_mean",
    text_auto=".4f",
    title="[DecisionTree 분류 모델] 평가용 데이터 특성 중요도 Top5"
)
fig3.show()