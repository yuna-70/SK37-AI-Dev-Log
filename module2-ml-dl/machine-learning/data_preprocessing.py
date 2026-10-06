"""TIL: 데이터 전처리 - 인코딩, 스케일링, 구간화, query (2026-10-06) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# One-Hot Encoding

## 데이터 불러오기

### 파일 경로 설정
file_path = "iris_dataset.csv"

### DataFrame 생성
df_iris = pd.read_csv(file_path)

### 결과 확인
display(df_iris)

## 붓꽃 label 컬럼의 품종별 개수 확인 -> 인코딩 후 생성될 컬럼 수 예상
label_counts = df_iris["label"].value_counts()
print(f"정답 label 컬럼의 항목별 개수: \n{label_counts}")

## One-Hot Encoding 실행: pd.get_dummies(data=df, dtype=int) 사용
## dtype=int를 지정하지 않으면 True/False로 생성됨
df_onehot = pd.get_dummies(data=df_iris, dtype=int)

## 결과 확인 -> label 컬럼 1개가 label_setosa, label_versicolor, label_virginica 3개로 변환됨
display(df_onehot)

# Label Encoding

## df.replace() 함수 실행 -> 범주형 문자열을 0부터 n-1까지의 숫자로 변환
df_label = df_iris.replace({"setosa": 0, "versicolor": 1, "virginica": 2})
display(df_label)

# Scaling

## 데이터 생성: 단위 차이가 크게 나는 데이터 샘플
data = {
    "나이": [22, 25, 47, 38, 29],
    "연봉(만원)": [3000, 3500, 8500, 6000, 4200]
}

## DataFrame 생성
df_sample = pd.DataFrame(data=data)

## 결과 확인
display(df_sample)

## 정규화(Normalization): 범위를 0 ~ 1로 변환

### 필요한 도구(클래스) 임포트
from sklearn.preprocessing import MinMaxScaler

### 정규화 도구 생성 -> 최소값=0, 최대값=1로 변환
minmax_scaler = MinMaxScaler()

### fit_transform() 함수 -> 데이터 변환 -> 결과는 넘파이 배열
data_minmax = minmax_scaler.fit_transform(df_sample)
print(f"정규화 적용 결과(넘파이 배열): \n{data_minmax}")

print("-" * 80)

### 정규화 결과 -> DataFrame으로 변환 -> 어느 열이 어떤 컬럼인지 확인
df_minmax = pd.DataFrame(
    data=data_minmax,
    index=df_sample.index,
    columns=["나이_정규화", "연봉_정규화"]
)
print(f"정규화 적용 결과: \n{df_minmax}")

## 표준화(Standardization): 평균 0, 표준편차 1인 분포로 변환

### 필요한 도구(클래스) 임포트
from sklearn.preprocessing import StandardScaler

### 표준화 도구 생성
standard_scaler = StandardScaler()

### fit_transform() 함수 -> 데이터 변환
data_standard = standard_scaler.fit_transform(df_sample)
print(f"표준화 적용 결과(넘파이 배열): \n{data_standard}")

print("-" * 80)

### 표준화 결과 -> DataFrame으로 변환
df_standard = pd.DataFrame(
    data=data_standard,
    index=df_sample.index,
    columns=["나이_표준화", "연봉_표준화"]
)
print(f"표준화 적용 결과: \n{df_standard}")

# 구간화(Binning)

## 데이터 생성(파이썬 딕셔너리)
data = {
    "age": [1, 10, 15, 13, 21, 23, 37, 31, 43, 80, 61, 20, 41, 32, 100],
    "gender": ["male", "male", "female", "female", "female", "male", "male", "female",
               "female", "female", "male", "male", "female", "female", "female"]
}

## 파이썬 딕셔너리 -> DataFrame으로 변환(key: 컬럼 이름, value: 컬럼의 값)
df_age = pd.DataFrame(data=data)
display(df_age)

print("-" * 80)

## age 컬럼 -> 구간 경계값과 label 설정
## bins는 경계값이므로 labels보다 1개 많아야 함 (경계 6개 -> 구간 5개)
age_bins = [0, 12, 19, 49, 70, 1000]
age_label = ["어린이", "청소년", "청년", "중년", "노년"]

## 목표: 구간화 한 결과 -> 새로운 컬럼(age_step)으로 추가
df_age["age_step"] = pd.cut(x=df_age["age"], bins=age_bins, labels=age_label)

## 결과 확인
display(df_age)

# query() 함수

## 샘플 데이터 생성
data = {
    "Name": ["Alice", "Bob", "Charlie", "David", "Eva"],
    "Age": [25, 30, 35, 22, 28],
    "Salary": [5000, 7000, 4500, 8000, 6000],
    "Dept": ["HR", "IT", "HR", "IT", "Marketing"]
}

## 파이썬 딕셔너리 -> DataFrame 생성
df_emp = pd.DataFrame(data=data)

## 결과 확인
display(df_emp)

## 기본 비교 연산자 사용

### 나이가 28세 이상인 행 필터링(추출)
df_emp1 = df_emp.query("Age >= 28")
display(df_emp1)

print("-" * 80)

### 부서(Dept)가 "IT"인 행 필터링(추출)
### 바깥이 큰따옴표이므로 안쪽 문자열은 작은따옴표 사용
df_emp2 = df_emp.query("Dept == 'IT'")
display(df_emp2)

## 논리 연산자 적용

### 나이가 25세 이상이면서 급여가 6000 이상인 행 -> 두 조건을 동시에 만족(&)
df_emp3 = df_emp.query("Age >= 25 & Salary >= 6000")
print("나이가 25세 이상이면서 급여가 6000 이상인 데이터")
display(df_emp3)

print("-" * 80)

### 부서가 "HR"이거나 급여가 7000 이상인 행 -> 둘 중 하나라도 만족(|)
df_emp4 = df_emp.query("Dept == 'HR' | Salary >= 7000")
print("부서가 HR이거나 급여가 7000 이상인 데이터")
display(df_emp4)

# query() 함수 연습 문제: ad_performance.csv

## 데이터 불러오기
file_path = "ad_performance.csv"
df_ad = pd.read_csv(file_path)

## 결과 확인
display(df_ad)

## 단일 조건: 문자열 적용
## 목표: Channel 컬럼의 값이 "Facebook"과 같은 행 추출
df_ad1 = df_ad.query("Channel == 'Facebook'")
display(df_ad1)

## 단일 조건: 숫자 적용
## 목표: Revenue 컬럼의 값이 1500000 이상인 행 추출
df_ad2 = df_ad.query("Revenue >= 1500000")
display(df_ad2)

## 다중 조건(논리 연산자 적용)
## 목표: Channel 컬럼의 값이 "Google"이면서 총매출이 1500000 이상인 행 추출
df_ad3 = df_ad.query("(Channel == 'Google') & (Revenue >= 1500000)")
display(df_ad3)