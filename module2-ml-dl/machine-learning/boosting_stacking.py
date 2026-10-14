"""TIL: XGBoost·스태킹 - 당뇨병 분류와 보스턴 집값 예측 (2026-10-14) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, root_mean_squared_error

# 분류: 당뇨병 여부 (RandomForest / XGBoost / Stacking 비교)

## 데이터 불러오기
diabetes_path = "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
df_diabetes = pd.read_csv(diabetes_path)
display(df_diabetes)

## X_data / y_data 생성
X_data = df_diabetes.drop(columns=["Diabetes_binary"])
y_data = df_diabetes["Diabetes_binary"]

## 80:20으로 학습용과 평가용 데이터 생성
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터의 정답 비율 확인
y_train_ratios = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답의 항목별 비율: \n{y_train_ratios}")

## RandomForest 분류 모델 (베깅)
from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(random_state=0)
rf_clf.fit(X_train, y_train)
pred_test_rf = rf_clf.predict(X_test)
accuracy_rf = accuracy_score(y_test, pred_test_rf)
print(f"RandomForest 성능(accuracy): {accuracy_rf}")

## XGBoost 분류 모델 (부스팅) -> 이전 트리의 잔차를 다음 트리가 학습
from xgboost import XGBClassifier

xgb_clf = XGBClassifier(random_state=0)
xgb_clf.fit(X_train, y_train)
pred_test_xgb = xgb_clf.predict(X_test)
accuracy_xgb = accuracy_score(y_test, pred_test_xgb)
print(f"XGBoost 성능(accuracy): {accuracy_xgb}")

## Stacking 분류 모델

### 1단계: 개별 기본 모델(Base Estimators) 생성
from sklearn.ensemble import StackingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression

base_estimators = [
    ("rf", RandomForestClassifier(random_state=0)),
    ("xgb", XGBClassifier(random_state=0)),
    ("dt", DecisionTreeClassifier(random_state=0))
]

### 2단계: 최종 메타 모델 생성 -> 1단계 모델들의 예측값을 입력으로 받음
final_meta = LogisticRegression(max_iter=1000)

### Stacking 모델 생성
stack_clf = StackingClassifier(
    estimators=base_estimators,
    final_estimator=final_meta
)

### 모델 학습(1단계 기본 모델 학습 및 예측 생성 -> 2단계 메타 모델 학습)
stack_clf.fit(X_train, y_train)
pred_test_stack = stack_clf.predict(X_test)
accuracy_stack = accuracy_score(y_test, pred_test_stack)
print(f"Stacking 성능(accuracy): {accuracy_stack}")

## 세 모델 성능 비교
print(f"RandomForest: {accuracy_rf}")
print(f"XGBoost: {accuracy_xgb}")
print(f"Stacking: {accuracy_stack}")

# 회귀: 보스턴 집값 (RandomForest / XGBoost / Stacking 비교)

## 데이터 불러오기
house_path = "house_price.csv"
df_house = pd.read_csv(house_path)

## X_data / y_data 생성
X_data_house = df_house.drop(columns=["medv"])
y_data_house = df_house["medv"]

## 75:25의 비율로 학습용 데이터와 평가용 데이터 생성
### 회귀는 정답이 연속형 숫자라 stratify를 적용할 수 없음
X_train_house, X_test_house, y_train_house, y_test_house = train_test_split(
    X_data_house,
    y_data_house,
    test_size=0.25,
    random_state=0
)

## RandomForest 회귀 모델
from sklearn.ensemble import RandomForestRegressor

rf_reg = RandomForestRegressor(random_state=0)
rf_reg.fit(X_train_house, y_train_house)
pred_test_rf_reg = rf_reg.predict(X_test_house)
rmse_rf = root_mean_squared_error(y_test_house, pred_test_rf_reg)
print(f"RandomForest 성능(RMSE): {rmse_rf}")

## XGBoost 회귀 모델
from xgboost import XGBRegressor

xgb_reg = XGBRegressor(random_state=0)
xgb_reg.fit(X_train_house, y_train_house)
pred_test_xgb_reg = xgb_reg.predict(X_test_house)
rmse_xgb = root_mean_squared_error(y_test_house, pred_test_xgb_reg)
print(f"XGBoost 성능(RMSE): {rmse_xgb}")

## Stacking 회귀 모델
from sklearn.ensemble import StackingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

### 1단계: 개별 기본 모델 생성
base_estimators_reg = [
    ("dt", DecisionTreeRegressor(random_state=0)),
    ("rf", RandomForestRegressor(random_state=0)),
    ("xgb", XGBRegressor(random_state=0))
]

### 2단계: 최종 메타 모델 생성 -> 회귀는 선형 회귀 모델 사용
final_meta_reg = LinearRegression()

stack_reg = StackingRegressor(
    estimators=base_estimators_reg,
    final_estimator=final_meta_reg
)

stack_reg.fit(X_train_house, y_train_house)
pred_test_stack_reg = stack_reg.predict(X_test_house)
rmse_stack = root_mean_squared_error(y_test_house, pred_test_stack_reg)
print(f"Stacking 성능(RMSE): {rmse_stack}")

## 세 모델 성능 비교
print(f"RandomForest: {rmse_rf}")
print(f"XGBoost: {rmse_xgb}")
print(f"Stacking: {rmse_stack}")