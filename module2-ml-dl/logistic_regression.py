"""TIL: 로지스틱 회귀 - 타이타닉 생존 여부 예측 (2026-10-08) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 전처리 실습: concat 함수

## 딕셔너리 자료형 데이터 생성
data1 = {"A": ["A0", "A1", "A2", "A3"],
         "B": ["B0", "B1", "B2", "B3"],
         "C": ["C0", "C1", "C2", "C3"],
         "D": ["D0", "D1", "D2", "D3"]}

data2 = {"A": ["A4", "A5", "A6", "A7", "A8"],
         "B": ["B4", "B5", "B6", "B7", "B8"],
         "C": ["C4", "C5", "C6", "C7", "C8"],
         "D": ["D4", "D5", "D6", "D7", "D8"]}

data3 = {"A": ["A9", "A10", "A11", "A12"],
         "B": ["B9", "B10", "B11", "B12"],
         "C": ["C9", "C10", "C11", "C12"],
         "D": ["D9", "D10", "D11", "D12"]}

## 데이터프레임 생성
df1 = pd.DataFrame(data=data1)
df2 = pd.DataFrame(data=data2)
df3 = pd.DataFrame(data=data3)

## 병합 실행 -> ignore_index=True: 원본 인덱스를 버리고 0부터 다시 부여
df_concat = pd.concat([df1, df2, df3], ignore_index=True)
display(df_concat)

# 데이터 불러오기

## 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

## 파일 경로 설정
train_path = "titanic_train.csv"
test_path = "titanic_test.csv"

## DataFrame 생성
df_train = pd.read_csv(train_path)
df_test = pd.read_csv(test_path)
display(df_train)
display(df_test)

# 데이터 전처리

## 데이터 병합: concat 함수 -> 891명 + 418명 = 1,309명
df_titanic = pd.concat([df_train, df_test], ignore_index=True)
display(df_titanic)

## 누락 데이터 처리

### 각 컬럼별 누락 데이터의 수 확인 -> df.isnull().sum()
num_nulls = df_titanic.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

### Cabin 컬럼: 누락이 1,014개(77%) -> 특정 컬럼 제거 -> drop 함수
df1 = df_titanic.drop(columns=["Cabin"])
display(df1)

### Age 컬럼: 연령별 분포 확인 -> value_counts()
age_counts = df1["Age"].value_counts().head(n=10)
print(f"Age 컬럼의 연령별 분포 Top 10: \n{age_counts}")

### Age 컬럼: 숫자값 컬럼 -> 누락 데이터 대체 -> 중간값 또는 최빈수 사용
age_stats = df1["Age"].describe()
print(f"Age 컬럼의 요약 통계량: \n{age_stats}")

### 중간값 추출 -> median() 함수
age_med = df1["Age"].median()
print(f"Age 컬럼의 중간값: {age_med}")

### fillna() 함수 -> 누락 대체
df1["Age"] = df1["Age"].fillna(age_med)
age_num_nulls = df1["Age"].isnull().sum()
print(f"Age 컬럼의 누락 데이터의 수: {age_num_nulls}")

### Age 컬럼: 구간화 -> 8단계
age_labels = [0, 1, 2, 3, 4, 5, 6, 7]
df1["Age_step"] = pd.cut(x=df1["Age"], bins=8, labels=age_labels)
display(df1)

### Embarked 컬럼: 항구별 빈도수 / 비율 추출
embarked_counts = df1["Embarked"].value_counts()
print(f"승선 항구별 빈도수: \n{embarked_counts}")

embarked_ratios = df1["Embarked"].value_counts(normalize=True)
print(f"승선 항구별 비율: \n{embarked_ratios}")

### Embarked 컬럼: 최빈값(빈도가 최대인 데이터)으로 채우기
df1["Embarked"] = df1["Embarked"].fillna("S")
embarked_num_nulls = df1["Embarked"].isnull().sum()
print(f"Embarked 컬럼의 누락 데이터의 수: {embarked_num_nulls}")

### Fare 컬럼: 항목별 빈도수 측정
fare_counts = df1["Fare"].value_counts()
print(f"요금별 빈도수: \n{fare_counts}")

### Fare 컬럼: 누락이 1개뿐 -> 삭제 -> dropna(subset=[col1, col2, ...])
df2 = df1.dropna(subset=["Fare"], ignore_index=True)
display(df2)

fare_num_nulls = df2["Fare"].isnull().sum()
print(f"Fare 컬럼의 누락 데이터의 수: {fare_num_nulls}")

## 이상치 처리: Fare 컬럼

### boxplot을 이용, Fare 컬럼 분포 확인
import plotly.express as px

fig_fare_before = px.box(data_frame=df2, y="Fare")
fig_fare_before.show()

### Fare 컬럼에 대한 Q1, Q3, IQR 계산
q1 = df2["Fare"].quantile(q=0.25)
q3 = df2["Fare"].quantile(q=0.75)
iqr = q3 - q1
print(f"Fare 컬럼 1사분위 값 q1: {q1}")
print(f"Fare 컬럼 3사분위 값 q3: {q3}")
print(f"Fare 컬럼 iqr: {iqr}")

### Fare 컬럼의 정상 범위 최소값 / 최대값 계산
min_val = q1 - (1.5 * iqr)
max_val = q3 + (1.5 * iqr)
print(f"Fare 컬럼 정상 범위의 최소값: {min_val}")
print(f"Fare 컬럼 정상 범위의 최대값: {max_val}")

### clip()을 통해 하한값 미만은 min_val로, 상한값 초과는 max_val로 일괄 대체
df2["Fare"] = df2["Fare"].clip(lower=min_val, upper=max_val)

fig_fare_after = px.box(data_frame=df2, y="Fare")
fig_fare_after.show()

## 불필요한 컬럼 삭제 -> PassengerId, Name, Age, Ticket
df3 = df2.drop(columns=["PassengerId", "Name", "Age", "Ticket"])
display(df3)

## One-Hot Encoding: 문자열로 된 특성 컬럼
df4 = pd.get_dummies(data=df3, columns=["Gender", "Embarked"], dtype=int)
display(df4)

## 결과 저장하기 -> df.to_csv(file_path, index=False)
file_path = "titanic_cleaned.csv"
df4.to_csv(file_path, index=False)

# 학습용 데이터와 평가용 데이터 생성

## 저장한 데이터 불러오기
df_cleaned = pd.read_csv(file_path)
display(df_cleaned)

## X_data 생성 -> 정답 컬럼을 제외한 나머지 컬럼들
X_data = df_cleaned.drop(columns="Survived")
display(X_data)

## y_data 생성 -> 정답 컬럼만 인덱싱
y_data = df_cleaned["Survived"]
print(f"정답 데이터(Survived): \n{y_data}")

## 정답 컬럼 -> 항목별 빈도수 / 비율 확인 -> 균등 또는 불균등 확인
y_counts = y_data.value_counts()
print(f"정답의 항목별 빈도수: \n{y_counts}")

y_ratios = y_data.value_counts(normalize=True)
print(f"정답의 항목별 비율: \n{y_ratios}")

## 80:20의 비율로 학습용 데이터와 평가용 데이터 생성
from sklearn.model_selection import train_test_split

### train_test_split 함수 호출(원본 정답의 비율 유지 -> stratify 적용)
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터 확인 -> 행 인덱스 확인 -> df.index
print(f"X_train의 index: \n{X_train.index}")
print(f"y_train의 index: \n{y_train.index}")

## 학습용 데이터의 정답 비율 <-> 원본 데이터의 정답 비율과 비교
y_train_ratios = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답의 항목별 비율: \n{y_train_ratios}")

# 표준화

## 필요한 도구 임포트
from sklearn.preprocessing import StandardScaler

## 도구 생성
standard_scaler = StandardScaler()

## 표준화 실행(DataFrame -> 2차원 배열)
### 학습용 -> fit_transform() 함수 -> 학습용 데이터의 평균과 표준 편차 계산해서 적용
### 평가용 -> transform() 함수 -> 학습용 데이터의 평균과 표준 편차 기준 적용
X_train_scaled = standard_scaler.fit_transform(X_train)
X_test_scaled = standard_scaler.transform(X_test)

# LogisticRegression 모델

## 모델 생성
from sklearn.linear_model import LogisticRegression

logistic = LogisticRegression()

## 모델 학습
logistic.fit(X_train_scaled, y_train)
print("학습 완료")

## 학습 결과 확인: 결정 경계(직선)의 기울기 / 절편
print(f"결정 경계 직선의 기울기: \n{logistic.coef_}")
print(f"결정 경계 직선의 절편: {logistic.intercept_}")

## 기울기를 컬럼명과 묶어서 특성별 영향력 확인
coef_features = pd.Series(data=logistic.coef_[0], index=X_data.columns)
print(f"특성별 기울기(영향력 순): \n{coef_features.sort_values(key=abs, ascending=False)}")

# 평가용 데이터를 이용한 예측

## 평가용 데이터를 이용한 생존 여부 예측(1과 0으로 분류)
pred_test = logistic.predict(X_test_scaled)
print(f"평가용 데이터에 대한 예측값: \n{pred_test}")

## 평가용 데이터에 대한 정답(y_test)
print(f"평가용 데이터에 대한 정답: \n{y_test}")

## 0과 1로 분류되기 전의 확률 확인 -> predict_proba()
pred_proba = logistic.predict_proba(X_test_scaled)
print(f"평가용 데이터에 대한 예측 확률(사망 / 생존): \n{pred_proba[:5]}")

# 모델 평가

## 필요한 함수 임포트
from sklearn.metrics import accuracy_score

## 평가용 데이터에 대한 성능 accuracy(정확도) 평가
accuracy = accuracy_score(y_test, pred_test)
print(f"평가용 데이터에 대한 성능(accuracy): {accuracy}")