"""TIL: 결정 트리 분류·회귀 - 당뇨병 여부 분류와 보스턴 집값 예측 (2026-10-13) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd
from sklearn.model_selection import train_test_split

# DecisionTree 분류 모델: 당뇨병 여부 분류

## 데이터 불러오기
diabetes_path = "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
df_diabetes = pd.read_csv(diabetes_path)
display(df_diabetes)

## X_data 생성 -> 정답 컬럼 제거
X_data = df_diabetes.drop(columns=["Diabetes_binary"])
display(X_data)

## y_data 생성 -> 정답 컬럼 인덱싱
y_data = df_diabetes["Diabetes_binary"]
print(f"정답 데이터(Diabetes_binary): \n{y_data}")

## 80:20으로 학습용과 평가용 데이터 생성
### train_test_split() 함수 호출 -> random_state, stratify 적용 -> 무작위성 통제
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터 확인 -> 행 인덱스 확인
print(f"X_train의 행 인덱스: \n{X_train.index}")
print(f"y_train의 행 인덱스: \n{y_train.index}")

## 정답의 항목별 비율 확인 -> 5050split 데이터라 50:50에 가까움
y_train_ratios = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답의 항목별 비율: \n{y_train_ratios}")

## 모델 생성 -> random_state -> 의사 결정 트리 생성의 무작위성 통제
from sklearn.tree import DecisionTreeClassifier

dt_clf = DecisionTreeClassifier(random_state=0)

## 모델 학습
dt_clf.fit(X_train, y_train)
print("학습 완료")

## 학습 시 생성된 의사 결정 트리의 최대 깊이 확인 -> model.get_depth()
print(f"학습된 모델의 최대 깊이: {dt_clf.get_depth()}")
print(f"리프 노드의 수: {dt_clf.get_n_leaves()}")

## 트리 구조 시각화 -> 깊이가 깊어 max_depth로 상위 3단계만 출력
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

plt.figure(figsize=(15, 10))
plot_tree(decision_tree=dt_clf, feature_names=X_train.columns, max_depth=3)
plt.show()

## 평가용 데이터를 이용한 예측
pred_test_dt_clf = dt_clf.predict(X_test)
print(f"평가용 데이터에 대한 예측의 결과: \n{pred_test_dt_clf}")

## 모델 평가
from sklearn.metrics import accuracy_score

### 과대적합 확인 -> 학습용과 평가용 성능을 함께 비교
accuracy_train = accuracy_score(y_train, dt_clf.predict(X_train))
accuracy_dt_clf = accuracy_score(y_test, pred_test_dt_clf)
print(f"학습용 데이터에 대한 성능(accuracy): {accuracy_train}")
print(f"평가용 데이터에 대한 성능(accuracy): {accuracy_dt_clf}")

# DecisionTree 회귀 모델: 보스턴 집값 예측

## 데이터 불러오기
house_path = "house_price.csv"
df_house = pd.read_csv(house_path)
display(df_house)

## X_data 생성 -> 정답 컬럼 삭제
X_data_house = df_house.drop(columns=["medv"])
display(X_data_house)

## y_data 생성 -> 정답 컬럼 인덱싱
y_data_house = df_house["medv"]
print(f"정답 데이터(medv): \n{y_data_house}")

## 75:25의 비율로 학습용 데이터와 평가용 데이터 생성
### 회귀는 정답이 연속형 숫자라 stratify를 적용할 수 없음
X_train_house, X_test_house, y_train_house, y_test_house = train_test_split(
    X_data_house,
    y_data_house,
    test_size=0.25,
    random_state=0
)

## 학습용 데이터 확인 -> 행 인덱스 확인
print(f"X_train의 행 인덱스: \n{X_train_house.index}")
print(f"y_train의 행 인덱스: \n{y_train_house.index}")

## 모델 생성
from sklearn.tree import DecisionTreeRegressor

dt_reg = DecisionTreeRegressor(random_state=0)

## 모델 학습
dt_reg.fit(X_train_house, y_train_house)
print("학습 완료")

## 학습 시 생성된 의사 결정 트리의 최대 깊이 확인
print(f"학습된 모델의 최대 깊이: {dt_reg.get_depth()}")

## 트리 구조 시각화 -> 상위 3단계만 출력
plt.figure(figsize=(15, 10))
plot_tree(decision_tree=dt_reg, feature_names=X_train_house.columns, max_depth=3)
plt.show()

## 평가용 데이터를 이용한 예측
pred_test_dt_reg = dt_reg.predict(X_test_house)
print(f"평가용 데이터에 대한 예측의 결과: \n{pred_test_dt_reg}")

## 모델 평가
from sklearn.metrics import root_mean_squared_error

### 과대적합 확인 -> 학습용 RMSE가 0에 가까우면 데이터를 외운 것
rmse_train = root_mean_squared_error(y_train_house, dt_reg.predict(X_train_house))
rmse_test_dt_reg = root_mean_squared_error(y_test_house, pred_test_dt_reg)
print(f"학습용 데이터에 대한 성능(RMSE): {rmse_train}")
print(f"평가용 데이터에 대한 성능(RMSE): {rmse_test_dt_reg}")