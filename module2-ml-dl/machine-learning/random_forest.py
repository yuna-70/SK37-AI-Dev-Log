"""TIL: 랜덤 포레스트 분류·회귀 - 당뇨병 여부 분류와 보스턴 집값 예측 (2026-10-13) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd
from sklearn.model_selection import train_test_split

# RandomForest 분류 모델: 당뇨병 여부 분류

## 데이터 불러오기
diabetes_path = "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
df_diabetes = pd.read_csv(diabetes_path)
display(df_diabetes)

## X_data 생성 -> 정답 컬럼 제거
X_data = df_diabetes.drop(columns=["Diabetes_binary"])

## y_data 생성 -> 정답 컬럼 인덱싱
y_data = df_diabetes["Diabetes_binary"]

## 80:20으로 학습용과 평가용 데이터 생성 -> 결정 트리와 같은 조건으로 분할
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 모델 생성 -> random_state -> 모델 생성의 무작위성 통제
from sklearn.ensemble import RandomForestClassifier

rf_clf = RandomForestClassifier(random_state=0)

## 모델 학습 -> 서로 다른 샘플과 특성으로 학습한 트리 여러 개를 생성
rf_clf.fit(X_train, y_train)
print("학습 완료")

## 생성된 트리의 개수 확인 -> n_estimators 기본값
print(f"생성된 트리의 개수: {rf_clf.n_estimators}")

## 평가용 데이터에 대한 예측 -> 트리들의 다수결로 최종 클래스 결정
pred_test_rf_clf = rf_clf.predict(X_test)
print(f"평가용 데이터에 대한 예측의 결과: \n{pred_test_rf_clf}")

## 모델 평가
from sklearn.metrics import accuracy_score

accuracy_rf_clf = accuracy_score(y_test, pred_test_rf_clf)
print(f"평가용 데이터에 대한 성능(accuracy): {accuracy_rf_clf}")

## 특성별 중요도 확인 -> 어떤 건강 지표가 당뇨병 분류에 기여했는가
importances = pd.Series(data=rf_clf.feature_importances_, index=X_data.columns)
print(f"특성별 중요도(상위 7개): \n{importances.sort_values(ascending=False).head(n=7)}")

# RandomForest 회귀 모델: 보스턴 집값 예측

## 데이터 불러오기
house_path = "house_price.csv"
df_house = pd.read_csv(house_path)
display(df_house)

## X_data 생성 -> 정답 컬럼 삭제
X_data_house = df_house.drop(columns=["medv"])

## y_data 생성 -> 정답 컬럼 인덱싱
y_data_house = df_house["medv"]

## 75:25의 비율로 학습용 데이터와 평가용 데이터 생성
### 회귀는 정답이 연속형 숫자라 stratify를 적용할 수 없음
X_train_house, X_test_house, y_train_house, y_test_house = train_test_split(
    X_data_house,
    y_data_house,
    test_size=0.25,
    random_state=0
)

## 모델 생성
from sklearn.ensemble import RandomForestRegressor

rf_reg = RandomForestRegressor(random_state=0)

## 모델 학습
rf_reg.fit(X_train_house, y_train_house)
print("학습 완료")

## 평가용 데이터를 이용한 예측 -> 트리들의 예측값 평균으로 최종 예측값 결정
pred_test_rf_reg = rf_reg.predict(X_test_house)
print(f"평가용 데이터에 대한 예측의 결과: \n{pred_test_rf_reg}")

## 모델 평가
from sklearn.metrics import root_mean_squared_error

rmse_test_rf_reg = root_mean_squared_error(y_test_house, pred_test_rf_reg)
print(f"평가용 데이터에 대한 성능(RMSE): {rmse_test_rf_reg}")