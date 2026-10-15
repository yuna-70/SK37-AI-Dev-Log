"""TIL: 모델 정규화(L1 규제) - 보스턴 집값 예측 (2026-10-14) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기
file_path = "house_price.csv"
df_house = pd.read_csv(file_path)
display(df_house)

# 데이터 전처리

## 각 컬럼별 누락 데이터의 수 확인
num_nulls = df_house.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

# 학습용 데이터와 평가용 데이터 생성

## X_data 생성 -> 정답 컬럼을 제외한 나머지 컬럼들
X_data = df_house.drop(columns=["medv"])

## y_data 생성 -> 정답 컬럼만 인덱싱
y_data = df_house["medv"]

## 75:25의 비율로 학습용 데이터와 평가용 데이터 생성
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.25,
    random_state=0
)

# 표준화 -> 규제 모델은 가중치 크기에 벌점을 매기므로 스케일을 맞춰야 함
from sklearn.preprocessing import StandardScaler

standard_scaler = StandardScaler()
X_train_scaled = standard_scaler.fit_transform(X_train)
X_test_scaled = standard_scaler.transform(X_test)

# LinearRegression 모델 (규제 없음)

## 모델 생성 및 학습
from sklearn.linear_model import LinearRegression

lireg = LinearRegression()
lireg.fit(X_train_scaled, y_train)
print("학습 완료")

## 기울기 / 절편 확인
print(f"선형 회귀 모델의 기울기: \n{lireg.coef_}")
print(f"선형 회귀 모델의 절편: {lireg.intercept_}")

## 평가용 데이터에 대한 예측
pred_test_lireg = lireg.predict(X_test_scaled)

## 모델 평가
from sklearn.metrics import root_mean_squared_error

rmse_lireg = root_mean_squared_error(y_test, pred_test_lireg)
print(f"평가용 데이터에 대한 성능(RMSE): {rmse_lireg}")

# 규제: 단순화

## Lasso 모델 (L1 규제) -> 작은 가중치를 0으로 만들어 특성을 제거함
from sklearn.linear_model import Lasso

lasso = Lasso()
lasso.fit(X_train_scaled, y_train)
print("학습 완료")

## L1 규제가 적용된 기울기 / 절편 확인
print(f"L1 규제가 적용된 선형 회귀 모델의 기울기: \n{lasso.coef_}")
print(f"L1 규제가 적용된 선형 회귀 모델의 절편: {lasso.intercept_}")

## 어떤 특성이 0이 되었는지 컬럼명과 묶어서 확인
coef_lasso = pd.Series(data=lasso.coef_, index=X_data.columns)
print(f"0이 되어 제거된 특성: \n{coef_lasso[coef_lasso == 0].index.tolist()}")
print(f"살아남은 특성: \n{coef_lasso[coef_lasso != 0]}")

## 평가용 데이터에 대한 예측
pred_test_lasso = lasso.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test_lasso}")

## 모델 평가 -> 규제 전후 비교
rmse_lasso = root_mean_squared_error(y_test, pred_test_lasso)
print(f"평가용 데이터에 대한 성능(RMSE): {rmse_lasso}")


# Ridge 모델 (L2 규제) -> 가중치를 같은 비율로 줄여 0에 가깝게 만듦

## 모델 생성
from sklearn.linear_model import Ridge

ridge = Ridge()

## 모델 학습
ridge.fit(X_train_scaled, y_train)
print("학습 완료")

## L2 규제가 적용된 기울기 / 절편 확인
print(f"L2 규제가 적용된 선형 회귀 모델의 기울기: \n{ridge.coef_}")
print(f"L2 규제가 적용된 선형 회귀 모델의 절편: {ridge.intercept_}")

## 0이 된 특성의 수 확인 -> L1(Lasso)과 비교하기 위함
print(f"Lasso에서 0이 된 특성의 수: {(lasso.coef_ == 0).sum()}개")
print(f"Ridge에서 0이 된 특성의 수: {(ridge.coef_ == 0).sum()}개")

## 평가용 데이터를 이용한 예측
pred_test_ridge = ridge.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test_ridge}")

## 모델 평가 -> 세 모델 비교
rmse_ridge = root_mean_squared_error(y_test, pred_test_ridge)
print(f"평가용 데이터에 대한 성능(RMSE): {rmse_ridge:.4f}")

print(f"선형 회귀(규제 없음): {rmse_lireg:.4f}")
print(f"Lasso(L1 규제): {rmse_lasso:.4f}")
print(f"Ridge(L2 규제): {rmse_ridge:.4f}")