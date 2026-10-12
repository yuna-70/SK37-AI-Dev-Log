"""TIL: SVM 분류 모델 - 타이타닉 생존 여부 예측 (2026-10-12) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기 -> 전처리가 완료된 데이터 재사용
file_path = "titanic_cleaned.csv"
df_titanic = pd.read_csv(file_path)
display(df_titanic)

# 학습용 데이터와 평가용 데이터 생성

## X_data 생성 -> 정답 컬럼을 제외한 나머지 컬럼들
X_data = df_titanic.drop(columns=["Survived"])
display(X_data)

## y_data 생성 -> 정답 컬럼만 인덱싱
y_data = df_titanic["Survived"]
print(f"정답 데이터(Survived): \n{y_data}")

## 정답 label의 항목별 비율 확인 -> value_counts(normalize=True)
y_ratios = y_data.value_counts(normalize=True)
print(f"정답의 항목별 비율: \n{y_ratios}")

## 80:20의 비율로 학습용 데이터와 평가용 데이터 생성
from sklearn.model_selection import train_test_split

### train_test_split() 함수 적용 -> random_state, stratify -> 무작위성 통제
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터 확인 -> 행 인덱스 확인(df.index)
print(f"X_train의 행 인덱스: \n{X_train.index}")
print(f"y_train의 행 인덱스: \n{y_train.index}")

## 학습용 데이터의 정답 비율 확인 -> stratify 적용 결과 확인
y_train_ratios = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답의 항목별 비율: \n{y_train_ratios}")

# 표준화 -> SVM은 거리 기반 모델이라 반드시 필요

## 필요한 도구 임포트
from sklearn.preprocessing import StandardScaler

## 표준화 도구 생성
standard_scaler = StandardScaler()

## 학습용 데이터를 기준으로 평균과 표준 편차 계산 및 적용
X_train_scaled = standard_scaler.fit_transform(X_train)
X_test_scaled = standard_scaler.transform(X_test)

# SVC 모델

## 모델 생성
from sklearn.svm import SVC

svc = SVC()

## 모델 학습 -> 마진이 최대가 되는 결정 경계 탐색
svc.fit(X_train_scaled, y_train)
print("학습 완료")

## 서포트 벡터 확인 -> 결정 경계와 가장 가까운 데이터
print(f"학습용 데이터 수: {len(y_train)}")
print(f"서포트 벡터의 수: {len(svc.support_)}")

# 평가용 데이터를 이용한 예측
pred_test_svc = svc.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test_svc}")

# 모델 평가

## 필요한 함수 임포트
from sklearn.metrics import accuracy_score

## 평가용 데이터에 대한 성능 accuracy(정확도) 평가
accuracy_svc = accuracy_score(y_test, pred_test_svc)
print(f"평가용 데이터에 대한 성능(accuracy): {accuracy_svc}")