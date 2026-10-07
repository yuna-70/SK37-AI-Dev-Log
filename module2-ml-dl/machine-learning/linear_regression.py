"""TIL: 선형 회귀 - 보스턴 집값 예측 (2026-10-07) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기

## 파일 경로 설정
file_path = "house_price.csv"

## DataFrame 생성
df_house = pd.read_csv(file_path)
display(df_house)

# 데이터 전처리

## 누락 데이터 처리
### isnull() -> 누락 여부 확인(True / False) -> sum(): True의 수 합산
num_nulls = df_house.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

# 학습용 데이터와 평가용 데이터 생성

## X_data 생성 -> 정답 컬럼을 제외한 나머지 컬럼들 -> drop(columns=[col1, col2, ...]) 함수
X_data = df_house.drop(columns=["medv"])
display(X_data)

## y_data 생성 -> 정답 컬럼만 인덱싱
y_data = df_house["medv"]
print(f"정답 데이터(medv): \n{y_data}")

## 75:25의 비율로 학습용 데이터와 평가용 데이터 생성
from sklearn.model_selection import train_test_split

### train_test_split 함수 호출(무작위성에 대한 통제 -> random_state 적용)
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.25,
    random_state=0
)

## 학습용 데이터 확인 -> 행 인덱스 확인 -> df.index
print(f"X_train의 index: \n{X_train.index}")
print(f"y_train의 index: \n{y_train.index}")

# 학습용 데이터에 대한 표준화 처리

## 필요한 도구(클래스) 임포트
from sklearn.preprocessing import StandardScaler

## 도구 생성
standard_scaler = StandardScaler()

## 표준화 실행(DataFrame -> 2차원 배열)
### 학습용 -> fit_transform() 함수 -> 학습용 데이터의 평균과 표준 편차 계산해서 적용
### 평가용 -> transform() 함수 -> 학습용 데이터의 평균과 표준 편차 기준 적용
X_train_scaled = standard_scaler.fit_transform(X_train)
X_test_scaled = standard_scaler.transform(X_test)

# LinearRegression 모델

## 모델 생성
from sklearn.linear_model import LinearRegression

lireg = LinearRegression()

## 모델 학습: 학습용 데이터(379개) -> 오차(RMSE)가 최소인 직선 추출
lireg.fit(X_train_scaled, y_train)

## 학습의 결과 생성된 RMSE 최소인 선형 모델의 기울기 / 절편 확인
print(f"학습용 데이터에 대해서 RMSE가 최소인 선형 회귀 모델의 기울기: \n{lireg.coef_}")
print(f"학습용 데이터에 대해서 RMSE가 최소인 선형 회귀 모델의 절편: {lireg.intercept_}")

## 기울기를 컬럼명과 묶어서 특성별 영향력 확인
coef_features = pd.Series(data=lireg.coef_, index=X_data.columns)
print(f"특성별 기울기(영향력 순): \n{coef_features.sort_values(key=abs, ascending=False)}")

# 평가용 데이터를 이용한 예측

## 평가용 데이터에 대한 주택 가격 예측
pred_test = lireg.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test}")

## 평가용 데이터에 대한 정답(y_test)
print(f"평가용 데이터에 대한 정답: \n{y_test}")

# 모델 평가

## RMSE로 평가 -> 기능 구현 함수 -> root_mean_squared_error 함수 임포트
from sklearn.metrics import root_mean_squared_error

## 평가 함수(정답, 예측값) -> 127개 평가용 데이터에 대한 RMSE
rmse_test = root_mean_squared_error(y_test, pred_test)
print(f"평가용 데이터에 대한 성능(RMSE): {rmse_test}")