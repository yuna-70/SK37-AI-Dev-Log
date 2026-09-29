"""TIL: pandas 기초 (2026-09-29) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# DataFrame 자료형 생성: csv 파일 처리

## csv 파일 경로 생성
file_path = "ad_performance.csv"

## read_csv() 함수 호출 -> DataFrame 자료형 생성
df = pd.read_csv(file_path)

## 결과 확인
print(df)

# DataFrame 분해: DataFrame = 행 인덱스 + 컬럼 인덱스 + 값

## 행 인덱스 추출: 객체.index
info_index = df.index
print(f"DataFrame 행 인덱스: \n{info_index}")

print("-" * 80)

## 컬럼 인덱스 추출: 객체.columns
info_columns = df.columns
print(f"DataFrame 컬럼 인덱스: \n{info_columns}")

print("-" * 80)

## 값(데이터) 추출: 객체.values
info_values = df.values
print(f"DataFrame 값: \n{info_values}")

# 인덱싱

## 특정 컬럼 인덱싱: 변수["컬럼명(컬럼 인덱스)"] -> 결과: Series 자료형 생성
channel = df["Channel"]
print(channel)

print("-" * 80)

## fancy 인덱싱: df[["컬럼1", "컬럼3", ...]] -> 결과: DataFrame 생성
df1 = df[["Channel", "Clicks", "Revenue"]]
print(df1)

print("-" * 80)

## 특정 행과 컬럼 인덱싱: 행 인덱스 4, 컬럼 인덱스 "Revenue" -> df.loc[행, 열]
data = df.loc[4, "Revenue"]
print(f"행 인덱스: 4, 컬럼 인덱스: Revenue의 값: {data}")

# 새로운 컬럼 추가(파생 변수 생성)

## CTR(클릭률) 컬럼 추가
df["CTR"] = df["Clicks"] / df["Impressions"] * 100

## 결과 확인
print("새로운 컬럼 추가 후 데이터프레임")
print(df)

print("-" * 80)

## ROAS(Return On Ad Spend: 광고비 대비 매출액) 컬럼 추가
df["ROAS"] = df["Revenue"] / df["Cost"] * 100

## 결과 확인
print("새로운 컬럼 추가 후 데이터프레임")
print(df)

# value_counts() 함수

## 분석 목표: Channel 컬럼의 항목별 빈도수 분석 -> df["Channel"] 인덱싱
channel_counts = df["Channel"].value_counts()
print(f"Channel 컬럼의 항목별 빈도수 분석: \n{channel_counts}")