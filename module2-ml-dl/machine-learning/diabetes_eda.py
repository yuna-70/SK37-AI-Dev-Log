"""TIL: 당뇨병 건강 지표 EDA - 정답 분포와 위험 요인 관계 분석 (2026-10-14) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd
import plotly.express as px

# 데이터 불러오기
file_path = "diabetes_binary_5050split_health_indicators_BRFSS2015.csv"
df_diabetes = pd.read_csv(file_path)
display(df_diabetes)

# 1. 정답 레이블(당뇨병 여부) 분포 분석

## 정답 레이블의 빈도수 추출
label_counts = df_diabetes["Diabetes_binary"].value_counts()
print(f"정답 레이블의 항목별 빈도수: \n{label_counts}")

## Series -> DataFrame 변환 -> 행 인덱스를 컬럼으로 -> reset_index() 함수
df_label_counts = label_counts.reset_index()
display(df_label_counts)

## 0.0을 "0", 1.0을 "1"로 대체 -> 그래프 x축을 범주로 인식시키기 위함
df_label_counts = df_label_counts.replace({0.0: "0", 1.0: "1"})
display(df_label_counts)

## 수직 막대 그래프 생성 및 출력
fig_label = px.bar(
    data_frame=df_label_counts,
    x="Diabetes_binary",
    y="count",
    text_auto=True,
    color="Diabetes_binary",
    title="당뇨병 여부별 빈도수"
)
fig_label.show()

# 2. 당뇨병과 고혈압의 관계 분석

## HighBP 컬럼: 고혈압 여부 빈도수 추출
hbp_counts = df_diabetes["HighBP"].value_counts()
print(f"고혈압 여부 빈도수: \n{hbp_counts}")

## Series -> DataFrame 변환 후 0.0 / 1.0을 문자열로 대체
df_hbp_counts = hbp_counts.reset_index().replace({0.0: "0", 1.0: "1"})
display(df_hbp_counts)

## 고혈압 항목별 빈도수에 대한 수직 막대 그래프
fig_hbp = px.bar(
    data_frame=df_hbp_counts,
    x="HighBP",
    y="count",
    text_auto=True,
    color="HighBP",
    title="고혈압 여부별 빈도수"
)
fig_hbp.show()

## 당뇨병 여부별 고혈압 분포 비교 -> barmode="group"으로 나란히 배치
fig_hbp_diabetes = px.histogram(
    data_frame=df_diabetes,
    x="Diabetes_binary",
    color="HighBP",
    barmode="group",
    text_auto=True,
    title="당뇨병 여부별 고혈압 분포"
)
fig_hbp_diabetes.update_traces(marker_line_color="#f08081", marker_line_width=1)
fig_hbp_diabetes.show()

# 3. 당뇨병과 고지혈증의 관계 분석

## HighChol 컬럼: 항목별 빈도수 추출
df_hchol_counts = df_diabetes["HighChol"].value_counts().reset_index()
display(df_hchol_counts)

## 당뇨병 여부별 고지혈증 분포 비교
fig_hchol_diabetes = px.histogram(
    data_frame=df_diabetes,
    x="Diabetes_binary",
    color="HighChol",
    barmode="group",
    text_auto=True,
    title="당뇨병 여부별 고지혈증 분포"
)
fig_hchol_diabetes.update_traces(marker_line_color="#f08081", marker_line_width=1)
fig_hchol_diabetes.show()