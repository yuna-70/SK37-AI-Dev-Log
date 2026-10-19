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