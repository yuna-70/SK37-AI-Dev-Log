"""TIL: 데이터 탐색 연습 - weather.csv (2026-10-01) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기

## 파일 경로 설정
file_path = "weather.csv"

## DataFrame 생성
df_weather = pd.read_csv(file_path)

## 결과 확인
display(df_weather)

# 요약 통계량 구하기
df_stats = df_weather.describe()
display(df_stats.round(1))

# temp 컬럼에 대한 평균값 구하기

## 방법1: df.loc
temp_mean1 = df_stats.loc["mean", "temp"]
print(f"temp의 평균값: {temp_mean1:.1f}")

print("-" * 80)

## 방법2: mean() 함수
temp_mean2 = df_weather["temp"].mean()
print(f"temp의 평균값: {temp_mean2:.1f}")

# hum 컬럼에 대한 최소값 구하기

## 방법1: df.loc
hum_min1 = df_stats.loc["min", "hum"]
print(f"hum 컬럼에 대한 최소값: {int(hum_min1)}")

print("-" * 80)

## 방법2: min() 함수
hum_min2 = df_weather["hum"].min()
print(f"hum 컬럼에 대한 최소값: {hum_min2}")

# hum 컬럼에 대한 최대값 구하기

## 방법1: df.loc
hum_max1 = df_stats.loc["max", "hum"]
print(f"hum 컬럼에 대한 최대값: {int(hum_max1)}")

print("-" * 80)

## 방법2: max() 함수
hum_max2 = df_weather["hum"].max()
print(f"hum 컬럼에 대한 최대값: {hum_max2}")

# atm 컬럼에 대한 중간값 구하기

## 방법1: df.loc
atm_median1 = df_stats.loc["50%", "atm"]
print(f"atm 컬럼에 대한 중간값: {atm_median1}")

print("-" * 80)

## 방법2: median() 함수
atm_median2 = df_weather["atm"].median()
print(f"atm 컬럼에 대한 중간값: {atm_median2}")

# speed 컬럼에 대한 표준 편차 구하기

## 방법1: df.loc
speed_std1 = df_stats.loc["std", "speed"]
print(f"speed 컬럼에 대한 표준 편차: {speed_std1:.1f}")

print("-" * 80)

## 방법2: std() 함수
speed_std2 = df_weather["speed"].std()
print(f"speed 컬럼에 대한 표준 편차: {speed_std2:.1f}")

# 상관 분석: 상관 행렬 구하기
## 주의: 요약 통계량(df_stats)이 아니라 원본 DataFrame에 적용해야 함
df_corr = df_weather.corr(numeric_only=True)
print("상관 행렬:")
display(df_corr.round(4))

# 온도(temp) 컬럼과 습도(hum) 컬럼의 상관 관계 분석

## 방법1: df.loc
corr_temp_hum1 = df_corr.loc["temp", "hum"]
print(f"온도와 습도의 상관 관계: {corr_temp_hum1}")

print("-" * 80)

## 방법2: 팬시 인덱싱 & corr() 함수 사용
corr_temp_hum2 = df_weather[["temp", "hum"]].corr()
print("온도와 습도의 상관 관계:")
display(corr_temp_hum2)