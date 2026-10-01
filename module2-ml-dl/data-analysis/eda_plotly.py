"""TIL: 탐색적 데이터 분석(EDA) - plotly 시각화 (2026-10-01) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd
import plotly.express as px

# 파이썬 경고 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 데이터 불러오기

## 파일 경로 설정
file_path = "tips.csv"

## DataFrame 생성
df_tips = pd.read_csv(file_path)

## 결과 확인
display(df_tips)

## 컬럼 확인
print(df_tips.columns)

# 목표: 요금의 총합이 증가할수록 팁의 크기도 증가하는가? (요금의 총합과 팁의 관계 시각화)

## x축: 요금의 총합(total_bill) 컬럼 -> 크기 순(오름차순)으로 정렬
## 직선 그래프는 데이터 순서대로 점을 이으므로 정렬이 필요함
df_sorted = df_tips.sort_values(by="total_bill")
display(df_sorted)

## time 컬럼의 항목별 빈도수 측정 -> color로 나눌 선의 개수 확인
counts_time = df_tips["time"].value_counts()
print(f"식사 시간대별 빈도수: \n{counts_time}")

print("-" * 80)

## 그래프 생성 및 출력
fig1 = px.line(data_frame=df_sorted, x="total_bill", y="tip", color="time")
fig1.show()

## 그래프 저장 -> HTML 파일로 저장하면 인터랙티브 기능이 유지됨
fig1.write_html("line.html")