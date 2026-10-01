"""TIL: 데이터 탐색 - 요약 통계량과 상관 분석 (2026-10-01) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기

## 파일 경로 설정
file_path = "ad_performance.csv"

## DataFrame 생성
df_ad = pd.read_csv(file_path)

## 결과 확인
display(df_ad)

# 요약 통계량: 수치형 컬럼에 대한 8가지 통계량
df_stats = df_ad.describe()
print("요약된 8가지 통계량:")
display(df_stats.round(1))

# 목표: Cost 컬럼의 평균값 구하기

## 방법1: 요약 통계량 -> 인덱싱(행: mean, 열: Cost)
avg_cost1 = df_stats.loc["mean", "Cost"]
print(f"Cost 컬럼의 평균값: {avg_cost1:.1f}")

print("-" * 80)

## 방법2: mean() 함수 -> 특정 컬럼에 대한 평균
avg_cost2 = df_ad["Cost"].mean()
print(f"Cost 컬럼의 평균값: {avg_cost2:.1f}")

# 목표: Revenue 컬럼의 최소값 구하기

## 방법1: 요약 통계량 -> 인덱싱 -> df.loc[행, 열]
min_revenue1 = df_stats.loc["min", "Revenue"]
print(f"Revenue 컬럼의 최소값: {int(min_revenue1)}")

print("-" * 80)

## 방법2: min() 함수 -> 특정 컬럼에 대한 최소값
min_revenue2 = df_ad["Revenue"].min()
print(f"Revenue 컬럼의 최소값: {min_revenue2}")

# 목표: Revenue 컬럼의 최대값 구하기

## 방법1: 요약 통계량 -> 인덱싱 -> df.loc[행, 열]
max_revenue1 = df_stats.loc["max", "Revenue"]
print(f"Revenue 컬럼의 최대값: {int(max_revenue1)}")

print("-" * 80)

## 방법2: max() 함수 -> 특정 컬럼에 대한 최대값
max_revenue2 = df_ad["Revenue"].max()
print(f"Revenue 컬럼의 최대값: {max_revenue2}")

# 목표: Revenue 컬럼의 중앙값과 평균값 비교

## Revenue 컬럼의 중앙값 구하기

### 방법1: 요약 통계량 -> 인덱싱 -> df.loc[행, 열]
median_revenue1 = df_stats.loc["50%", "Revenue"]
print(f"Revenue 컬럼의 중앙값: {median_revenue1}")

print("-" * 80)

### 방법2: quantile(q=0.5) 함수 사용 -> 특정 컬럼의 중앙값
median_revenue2 = df_ad["Revenue"].quantile(q=0.5)
print(f"Revenue 컬럼의 중앙값: {median_revenue2}")

print("-" * 80)

### 방법3: median() 함수 사용 -> 특정 컬럼의 중앙값
median_revenue3 = df_ad["Revenue"].median()
print(f"Revenue 컬럼의 중앙값: {median_revenue3}")

print("-" * 80)

## Revenue 컬럼의 평균값 구하기

### 방법1: 요약 통계량 -> 인덱싱 -> df.loc["mean", "Revenue"]
avg_revenue1 = df_stats.loc["mean", "Revenue"]
print(f"Revenue 컬럼의 평균값: {avg_revenue1:.1f}")

print("-" * 80)

### 방법2: mean() 함수 사용 -> 특정 컬럼의 평균값
avg_revenue2 = df_ad["Revenue"].mean()
print(f"Revenue 컬럼의 평균값: {avg_revenue2:.1f}")

# 목표: Revenue 컬럼의 표준 편차 구하기

## 방법1: 요약 통계량 -> 인덱싱 -> df.loc["std", "Revenue"]
std_revenue1 = df_stats.loc["std", "Revenue"]
print(f"Revenue 컬럼의 표준 편차: {std_revenue1:.1f}")

print("-" * 80)

## 방법2: std() 함수 사용 -> 특정 컬럼의 표준 편차
std_revenue2 = df_ad["Revenue"].std()
print(f"Revenue 컬럼의 표준 편차: {std_revenue2:.1f}")

# 목표: Cost 컬럼의 행의 수 구하기

## 방법1: 요약 통계량 -> 인덱싱 -> df.loc["count", "Cost"]
count_cost1 = df_stats.loc["count", "Cost"]
print(f"Cost 컬럼의 행의 수: {int(count_cost1)}개")

print("-" * 80)

## 방법2: count() 함수 사용 -> 특정 컬럼의 행의 수(데이터의 수)
count_cost2 = df_ad["Cost"].count()
print(f"Cost 컬럼의 행의 수: {count_cost2}개")

print("-" * 80)

## 방법3: len() 함수 사용 -> 데이터프레임의 행의 수 또는 특정 컬럼의 행의 수
count_cost3 = len(df_ad["Cost"])
print(f"Cost 컬럼의 행의 수: {count_cost3}개")

# 상관 분석: 상관 행렬 구하기 -> 원본 DataFrame에 적용
df_corr = df_ad.corr(numeric_only=True)
print(f"데이터프레임에 대한 상관 행렬: \n{df_corr.round(2)}")

# 비용(Cost) 컬럼과 매출(Revenue) 컬럼의 상관 관계 분석

## 방법1: 상관 행렬 -> 인덱싱 -> 행: Cost, 열: Revenue
corr_cost_revenue1 = df_corr.loc["Cost", "Revenue"]
print(f"비용과 매출의 상관 관계(상관 계수): {corr_cost_revenue1}")

print("-" * 80)

## 방법2: 비용 컬럼과 매출 컬럼 -> 팬시 인덱싱 & 상관 분석
corr_cost_revenue2 = df_ad[["Cost", "Revenue"]].corr()
print(f"비용과 매출의 상관 관계(상관 계수): \n{corr_cost_revenue2}")