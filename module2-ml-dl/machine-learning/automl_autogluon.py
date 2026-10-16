"""TIL: AutoML - AutoGluon 고객 이탈 예측 (2026-10-16) — 개념 설명은 README.md 참고"""

# 데이터 불러오기

## 필요한 라이브러리 임포트
import pandas as pd

## 파일 경로 설정
file_path = "Telco-Customer-Churn.csv"

## DataFrame 생성
df = pd.read_csv(file_path)
display(df)

# 데이터 전처리

## TotalCharges 컬럼: 숫자로 변환할 수 없는 문자열인 행 제거

### 숫자로 변환할 수 없는 문자열인 행 -> 누락(NaN) 변환 처리
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")

### 누락인 행 제거
df1 = df.dropna(ignore_index=True)
print("TotalCharges 컬럼에서 문자열을 제거한 결과")
display(df1)

## 불필요한 컬럼 제거: 고객 식별자인 customerID 컬럼 제거
df2 = df1.drop(columns=["customerID"])
print("불필요한 컬럼을 제거한 결과")
display(df2)

# 학습용과 평가용 데이터 생성

## 필요한 함수 임포트
from sklearn.model_selection import train_test_split

## X_data, y_data로 나누지 않고 DataFrame 통째로 80:20 분할
### AutoGluon은 label 매개변수로 정답 컬럼을 지정하므로 X/y 분할이 불필요함
train_df, test_df = train_test_split(
    df2,
    test_size=0.2,
    random_state=0,
    stratify=df2["Churn"]
)

## 결과 확인(1): 학습용 데이터의 행 인덱스
print(f"학습용 데이터의 행 인덱스: \n{train_df.index}")

print("-" * 80)

## 결과 확인(2): stratify가 적용됐는지 학습용과 평가용의 정답 비율 비교
train_ratio = train_df["Churn"].value_counts(normalize=True)
test_ratio = test_df["Churn"].value_counts(normalize=True)
print(f"학습용 데이터의 정답 비율: \n{train_ratio}")
print(f"평가용 데이터의 정답 비율: \n{test_ratio}")

# 학습(best 모델 생성)

## 필요한 클래스 임포트
from autogluon.tabular import TabularPredictor

## 클래스 호출, 모델 생성
predictor = TabularPredictor(
    label="Churn",                  # 정답 컬럼
    eval_metric="accuracy",         # 평가 기준
    path="autogluon_churn_model"    # 학습된 모델 저장 경로
)

## 학습 및 고도화
predictor.fit(
    train_data=train_df,
    presets="best_quality",
    num_gpus=0,
    dynamic_stacking=False,   # 자원을 낭비하면 안 되니까 쓸데없는 것은 끄기
    num_stack_levels=1,       # stack은 1단계까지만
    time_limit=300
)

## 학습에 사용된 모든 모델 성능 비교
predictor.leaderboard()

## best 모델 확인
best_model_name = predictor.model_best
print(best_model_name)

# 평가용 데이터를 이용한 성능 평가

## evaluate(test_df) 함수 -> 예측 + 평가를 한 번에 수행
performance = predictor.evaluate(test_df)
print(f"고객 이탈 예측 데이터에 대한 분류 성능: \n{performance}")

# 저장된 모델 이용하기

## 모델 저장 경로 설정
model_path = "autogluon_churn_model"

## 저장된 모델(학습이 완료된 상태) 불러오기
loaded_predictor = TabularPredictor.load(model_path)

## 저장된 모델을 이용한 성능 평가
performance = loaded_predictor.evaluate(test_df)
print(f"저장된 모델을 이용한 성능 평가: \n{performance}")