"""TIL: 고객 이탈 예측 - Telco 데이터 전처리·EDA·분류 모델 (2026-10-15) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd
import plotly.express as px

# 데이터 불러오기
file_path = "Telco-Customer-Churn.csv"
df_telco = pd.read_csv(file_path)
display(df_telco)

# 데이터 전처리

## DataFrame의 기본 정보(행과 열, 자료형) 확인 -> info() 함수
df_telco.info()

## 문제점: TotalCharges 컬럼이 숫자가 아닌 문자열(str)로 읽힘

### TotalCharges 컬럼의 값이 공백 문자열(" ")인 행 인덱스 추출
space_index = df_telco.query("TotalCharges == ' '").index
print(f"공백 문자열이 들어 있는 행 인덱스: \n{space_index}")

### 1단계: 문자열 -> 숫자형으로 변환 -> pd.to_numeric()
### errors="coerce": 숫자로 바꿀 수 없는 값을 강제로 누락(NaN) 처리
df_telco["TotalCharges"] = pd.to_numeric(df_telco["TotalCharges"], errors="coerce")
print("빈 문자열 처리 후 info 함수 적용")
df_telco.info()

### 2단계: 누락이 된 행 제거 -> dropna()
df_cleaned = df_telco.dropna(ignore_index=True)
display(df_cleaned)

# 데이터 탐색 및 EDA

## 1. 정답 컬럼(Churn)의 항목별 분포 -> 원 그래프

### 전체 고객 중 이탈자의 비율 파악
df_churn_ratio = df_cleaned["Churn"].value_counts(normalize=True).reset_index()
display(df_churn_ratio)

fig_churn = px.pie(
    data_frame=df_churn_ratio,
    names="Churn",
    values="proportion",
    title="고객 이탈 여부 비중",
    hole=0.3
)
fig_churn.show()

## 2. 계약 형태(Contract)와 고객 이탈의 관계 -> 막대 그래프

### groupby의 기준 컬럼 2개 + 행의 수 연산(size) -> reset_index(name="컬럼명")
df_contract_churn = df_cleaned.groupby(by=["Contract", "Churn"]).size().reset_index(name="Count")
display(df_contract_churn)

fig_contract = px.bar(
    data_frame=df_contract_churn,
    x="Contract",
    y="Count",
    color="Churn",
    barmode="group",
    text_auto=True,
    title="계약 형태별 고객 이탈 여부 비교"
)
fig_contract.show()

## 3. 가입 기간(tenure)과 고객 이탈의 관계 -> 히스토그램
fig_tenure = px.histogram(
    data_frame=df_cleaned,
    x="tenure",
    color="Churn",
    barmode="group",
    title="가입 기간에 따른 이탈 분포"
)
fig_tenure.update_traces(marker_line_color="#f88080", marker_line_width=1)
fig_tenure.show()

## 4. 월 요금(MonthlyCharges)과 고객 이탈의 관계 -> 히스토그램
fig_monthly = px.histogram(
    data_frame=df_cleaned,
    x="MonthlyCharges",
    color="Churn",
    barmode="group",
    title="월 사용 요금과 고객 이탈의 관계"
)
fig_monthly.update_traces(marker_line_color="#f88080", marker_line_width=1)
fig_monthly.show()

## 5. 총 누적 요금(TotalCharges)과 고객 이탈의 관계 -> 히스토그램
fig_total = px.histogram(
    data_frame=df_cleaned,
    x="TotalCharges",
    color="Churn",
    barmode="group",
    title="총 누적 요금과 고객 이탈의 관계"
)
fig_total.update_traces(marker_line_color="#f88080", marker_line_width=1)
fig_total.show()

# Encoding

## 불필요한 컬럼 삭제 -> customerID는 고객 식별용이라 학습에서 제외
df_dropped = df_cleaned.drop(columns=["customerID"])
display(df_dropped)

## 정답 컬럼(Churn) -> Label Encoding ("No": 0, "Yes": 1) -> map() 함수
df_dropped["Churn"] = df_dropped["Churn"].map({"No": 0, "Yes": 1})
display(df_dropped)

## 특성 중 범주형 컬럼 -> One-Hot Encoding

### 범주형 컬럼 추출 -> df.select_dtypes() 함수
df_categorical = df_dropped.select_dtypes(include=["str"])
display(df_categorical)

### 범주형 컬럼의 이름 추출 -> df.columns
categorical_cols = df_categorical.columns
print(f"범주형 컬럼의 이름: \n{categorical_cols}")

### Index 자료형 -> 리스트 자료형으로 변환 -> tolist()
categorical_cols_list = categorical_cols.tolist()
print(f"범주형 컬럼 이름의 리스트: \n{categorical_cols_list}")

### 한 줄로 작성하면: df.select_dtypes(include=["str"]).columns.tolist()

### pd.get_dummies() 호출, 원-핫 인코딩 적용
df_onehot = pd.get_dummies(data=df_dropped, columns=categorical_cols_list, dtype=int)
display(df_onehot)

# 학습용 데이터와 평가용 데이터 생성

## X_data 생성 -> 정답 컬럼 제거
X_data = df_onehot.drop(columns=["Churn"])
display(X_data)

## y_data 생성 -> 정답 컬럼 인덱싱
y_data = df_onehot["Churn"]
print(f"정답 데이터(Churn): \n{y_data}")

## 정답의 항목별 비율 확인 -> 불균형 데이터인지 확인
y_ratios = y_data.value_counts(normalize=True)
print(f"정답 컬럼의 항목별 비율: \n{y_ratios}")

## 80:20의 비율로 학습용과 평가용 데이터 생성
from sklearn.model_selection import train_test_split

### 정답이 불균형이므로 stratify로 비율을 유지하며 분할
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터 확인 -> 행 인덱스
print(f"X_train의 행 인덱스: \n{X_train.index}")
print(f"y_train의 행 인덱스: \n{y_train.index}")

## 학습용 데이터의 정답 비율 확인 -> stratify 적용 결과 확인
y_train_ratios = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답의 항목별 비율: \n{y_train_ratios}")

# 표준화
## TotalCharges는 18.8~8684.8, 원-핫 컬럼은 0~1이라 값의 범위 차이가 매우 큼

## 필요한 도구 임포트
from sklearn.preprocessing import StandardScaler

standard_scaler = StandardScaler()
X_train_scaled = standard_scaler.fit_transform(X_train)
X_test_scaled = standard_scaler.transform(X_test)

# LogisticRegression(로지스틱 회귀) 분류 모델

## 모델 생성
from sklearn.linear_model import LogisticRegression

lr = LogisticRegression()

## 모델 학습: fit()
lr.fit(X_train_scaled, y_train)
print("학습 완료")

## 평가용 데이터에 대한 예측: predict()
pred_test_lr = lr.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test_lr}")

## 이탈로 예측한 고객의 수 확인 -> 한쪽으로만 예측하고 있지 않은지 확인
print(f"이탈(1)로 예측한 고객 수: {(pred_test_lr == 1).sum()}명 / 전체 {len(y_test)}명")

## 모델 평가: accuracy_score()
from sklearn.metrics import accuracy_score

accuracy_lr = accuracy_score(y_test, pred_test_lr)
print(f"LogisticRegression 모델의 정확도: {accuracy_lr:.4f}")

# SVM 분류 모델

## 모델 생성
from sklearn.svm import SVC

svc = SVC()

## 모델 학습: fit()
svc.fit(X_train_scaled, y_train)
print("학습 완료")

## 평가용 데이터를 이용한 예측: predict()
pred_test_svc = svc.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test_svc}")

## 이탈로 예측한 고객의 수 확인
print(f"이탈(1)로 예측한 고객 수: {(pred_test_svc == 1).sum()}명 / 전체 {len(y_test)}명")

## 모델 평가
accuracy_svc = accuracy_score(y_test, pred_test_svc)
print(f"SVM 모델의 정확도: {accuracy_svc:.4f}")

# 베이스라인과 비교 -> 전원을 '잔류'로 찍었을 때의 정확도
baseline = (y_test == 0).mean()
print(f"베이스라인(전원 잔류로 예측): {baseline:.4f}")
print(f"LogisticRegression: {accuracy_lr:.4f}")
print(f"SVM: {accuracy_svc:.4f}")

# DecisionTree 분류 모델
## 트리 기반 모델은 값의 순서만 보므로 표준화하지 않은 원본 데이터를 사용

## 모델 생성
from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=0)

## 모델 학습: fit()
dt.fit(X_train, y_train)
print("학습 완료")

## 생성된 트리의 구조 확인
print(f"트리의 깊이(depth): {dt.get_depth()}")
print(f"리프 노드의 수: {dt.get_n_leaves()}")

## 평가용 데이터를 이용한 예측: predict()
pred_test_dt = dt.predict(X_test)
print(f"평가용 데이터에 대한 예측값: \n{pred_test_dt}")

## 이탈로 예측한 고객의 수 확인
print(f"이탈(1)로 예측한 고객 수: {(pred_test_dt == 1).sum()}명 / 전체 {len(y_test)}명")

## 모델 평가 -> 과대적합 확인을 위해 학습용 성능도 함께 측정
accuracy_train_dt = accuracy_score(y_train, dt.predict(X_train))
accuracy_dt = accuracy_score(y_test, pred_test_dt)
print(f"DecisionTree 학습용 정확도: {accuracy_train_dt:.4f}")
print(f"DecisionTree 모델의 정확도: {accuracy_dt:.4f}")

## 특성별 중요도 확인 -> 어떤 특성이 이탈 예측에 기여했는가
importances = pd.Series(data=dt.feature_importances_, index=X_data.columns)
print(f"특성별 중요도(상위 7개): \n{importances.sort_values(ascending=False).head(n=7)}")

# 세 모델 성능 비교 -> 베이스라인과 함께
baseline = (y_test == 0).mean()
print(f"베이스라인(전원 잔류로 예측): {baseline:.4f}")
print(f"LogisticRegression: {accuracy_lr:.4f}")
print(f"SVM: {accuracy_svc:.4f}")
print(f"DecisionTree: {accuracy_dt:.4f}")