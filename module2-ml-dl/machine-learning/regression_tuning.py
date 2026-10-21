"""TIL: 회귀 모델 성능 고도화 - 보스턴 집값 (2026-10-21) — 개념 설명은 README.md 참고"""

# 파이썬 경고 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 데이터 불러오기

## 필요한 라이브러리 임포트
import pandas as pd

## 파일 경로 설정
file_path = "house_price.csv"

## DataFrame 생성
df = pd.read_csv(file_path)
display(df)

# 학습용과 평가용 데이터 생성

## 필요한 함수 임포트
from sklearn.model_selection import train_test_split

## X_data 생성 -> 정답 컬럼 제거
X_data = df.drop(columns=["medv"])
display(X_data)

## y_data 생성 -> 정답 컬럼 인덱싱
y_data = df["medv"]
print(y_data)

## 75:25의 비율로 분할 -> 무작위성 통제 -> random_state
### 회귀 문제이므로 stratify는 사용하지 않음(정답이 연속적인 숫자라 비율 유지가 불가능)
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.25,
    random_state=0
)

## 학습용 데이터의 인덱스 확인
print(X_train.index)
print(y_train.index)

# DecisionTree 회귀 모델 고도화

## 필요한 클래스 임포트
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import GridSearchCV

## 성능 고도화 대상 모델 생성
dt = DecisionTreeRegressor(random_state=0)

## 최적화 할 매개 변수와 탐색 조건 설정 -> 18 * 4 = 72가지 조합
params = {
    "max_depth": range(3, 21),
    "min_samples_leaf": [2, 3, 4, 5]
}

## 탐색 도구 생성
### 회귀의 평가 기준 -> neg_root_mean_squared_error(RMSE에 음수를 붙인 값)
grid_dt = GridSearchCV(
    estimator=dt,
    param_grid=params,
    scoring="neg_root_mean_squared_error",
    cv=5
)

## 탐색 도구 학습 및 검증
grid_dt.fit(X_train, y_train)
print("검증 완료")

## best 모델 추출
best_dt = grid_dt.best_estimator_
print(best_dt)

## 검증용 데이터에 대한 최적의 성능 확인 -> 음수로 출력됨
print(grid_dt.best_score_)

## 평가용 데이터에 대한 예측
pred_dt = best_dt.predict(X_test)
print(pred_dt)
print(f"평가용 데이터의 정답(실제 주택 가격): \n{y_test}")

## 모델 평가: RMSE

### 필요한 함수 임포트
from sklearn.metrics import root_mean_squared_error as rmse

### 평가용 데이터에 대한 정답과의 오차(RMSE) 측정
rmse_dt = rmse(y_test, pred_dt)
print(f"고도화 된 DecisionTree 회귀 모델의 성능(RMSE): {rmse_dt:.3f}")

# RandomForest 회귀 모델 고도화

## 필요한 클래스 임포트
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

## 성능 고도화 대상 모델 생성
rf = RandomForestRegressor(random_state=0)

## 최적화 할 매개 변수와 탐색 조건 설정 -> 5 * 28 * 4 = 560가지 조합
params = {
    "n_estimators": [100, 200, 300, 400, 500],
    "max_depth": range(3, 31),
    "min_samples_leaf": [2, 3, 4, 5]
}

## 탐색 도구 생성 -> 560가지 중 120가지만 무작위로 추출해서 탐색
random_rf = RandomizedSearchCV(
    estimator=rf,
    param_distributions=params,
    n_iter=120,
    scoring="neg_root_mean_squared_error",
    cv=5,
    random_state=0
)

## 학습 및 검증
random_rf.fit(X_train, y_train)
print("검증 완료")

## best 모델 추출
best_rf = random_rf.best_estimator_
print(best_rf)

## 검증용 데이터에 대한 최적의 성능 확인
print(random_rf.best_score_)

## 평가용 데이터에 대한 예측
pred_rf = best_rf.predict(X_test)
print(pred_rf)

## 모델 평가
rmse_rf = rmse(y_test, pred_rf)
print(f"고도화된 RandomForest 회귀 모델의 성능(RMSE): {rmse_rf:.3f}")