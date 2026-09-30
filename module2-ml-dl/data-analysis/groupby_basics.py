"""TIL: 중복 데이터 그룹화 (2026-09-30) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기

## 파일 경로 설정
file_path = "ad_performance.csv"

## DataFrame 생성
df_ad = pd.read_csv(file_path)

## 결과 확인
display(df_ad)

# Channel 컬럼의 항목별 빈도수 분석 -> 데이터 중복 확인

## 1단계: Channel 컬럼 인덱싱
channel = df_ad["Channel"]
print(channel)

print("-" * 80)

## 2단계: value_counts() 함수 적용
channel_counts = df_ad["Channel"].value_counts()
print(f"채널별 빈도수: \n{channel_counts}")

# 목표: 채널별 평균 매출 계산 및 비교
# -> groupby() 함수 적용 + 집계할 컬럼 선택 + 집계 함수 지정
channel_avg_rev = df_ad.groupby(by="Channel")["Revenue"].mean()
print(f"채널별 평균 매출: \n{channel_avg_rev.round()}")

# groupby().agg() 함수: 여러 개의 컬럼에 대해서 다양한 집계 함수 적용
channel_summary = df_ad.groupby(by="Channel").agg(
    total_cost=("Cost", "sum"),
    avg_cost=("Cost", "mean"),
    total_revenue=("Revenue", "sum"),
    avg_revenue=("Revenue", "mean")
)

print("분석 결과")
display(channel_summary.round(1))