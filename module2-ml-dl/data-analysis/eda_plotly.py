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

# ===== 2026-10-02 추가: 직선 그래프 이후 =====

# seaborn 라이브러리로 직선 그래프 그리기 -> 비교

## 필요한 라이브러리 임포트
import matplotlib.pyplot as plt
import seaborn as sns

## 목표: 요금의 총합이 증가할수록 팁의 크기도 증가하는가?
## seaborn 직선 그래프 -> 함수: lineplot(data, x, y)
sns.lineplot(data=df_tips, x="total_bill", y="tip")
plt.show()

print("-" * 80)

## plotly의 color 기능 -> seaborn에서는 매개변수 hue가 담당
sns.lineplot(data=df_tips, x="total_bill", y="tip", hue="time")
plt.show()

# 막대 그래프

## 시각화 목표: 요일 별 요금의 총합(total_bill) 평균값 시각화

## 통계 분석: 요일 별 그룹핑(groupby) + 요금의 총합 컬럼 지정 + 평균 함수 적용
day_mean = df_tips.groupby(by="day")["total_bill"].mean()
print(f"요일 별 평균 요금: \n{day_mean}")

print("-" * 80)

## Series 자료형 -> DataFrame 자료형 변환(행 인덱스 -> 컬럼 + 번호 행 인덱스 추가)
df_day_mean = day_mean.reset_index()
display(df_day_mean)

print("-" * 80)

## DataFrame -> 컬럼 이름 변경 -> rename()
df_day_mean1 = df_day_mean.rename(columns={"total_bill": "avg_total_bill"})
display(df_day_mean1)

## 그래프 생성 및 출력
fig_bar1 = px.bar(data_frame=df_day_mean1, x="day", y="avg_total_bill")
fig_bar1.show()

print("-" * 80)

## 그래프 x축 항목 -> 요일 별로 정렬(목, 금, 토, 일) -> 매개변수: category_orders
fig_bar2 = px.bar(
    data_frame=df_day_mean1,
    x="day",
    y="avg_total_bill",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]}
)
fig_bar2.show()

print("-" * 80)

## 요일별로 정렬 + 요일별로 색상 추가
fig_bar3 = px.bar(
    data_frame=df_day_mean1,
    x="day",
    y="avg_total_bill",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    color="day"
)
fig_bar3.show()

# 수평 막대 그래프

## 시각화 목표: 요일별 평균 요금(avg_total_bill) 비교
## 수평형 -> x가 수치형 컬럼, y가 범주형 컬럼 + orientation="h"
fig_bar_h = px.bar(
    data_frame=df_day_mean1,
    x="avg_total_bill",
    y="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    color="day",
    orientation="h"
)
fig_bar_h.show()

# 원 그래프

## 시각화 목표: 고객의 성별 빈도수를 비율로 비교

## 통계 분석: "sex" 컬럼 인덱싱 + value_counts(normalize=True) 함수 -> 비율 반환
sex_ratio = df_tips["sex"].value_counts(normalize=True)
print(f"고객의 성별 비율: \n{sex_ratio}")

print("-" * 80)

## Series 자료형 -> DataFrame 자료형 변환
df_sex_ratio = sex_ratio.reset_index()
display(df_sex_ratio)

print("-" * 80)

## 그래프 생성 및 출력 -> hole 지정 시 도넛 모양
fig_pie = px.pie(
    data_frame=df_sex_ratio,
    names="sex",
    values="proportion",
    hole=0.4
)
fig_pie.show()

# 수직 히스토그램

## 시각화 목표: total_bill 금액 구간별 누적 빈도수 비교
## 수직형 -> x가 수치형 컬럼, y=None (y축은 빈도수 자동 계산)
fig_hist_v1 = px.histogram(
    data_frame=df_tips,
    x="total_bill",
    y=None,
    nbins=50
)
fig_hist_v1.show()

print("-" * 80)

## 모든 막대에 일괄적으로 검은색 경계선 넣기
fig_hist_v1.update_traces(marker_line_color="black", marker_line_width=2)
fig_hist_v1.show()

print("-" * 80)

## color="time" 첨가 -> 식사 시간대별, 금액 구간별 누적 빈도수 분석
fig_hist_v2 = px.histogram(
    data_frame=df_tips,
    x="total_bill",
    color="time"
)
fig_hist_v2.update_traces(marker_line_color="#F5EE9D", marker_line_width=1)
fig_hist_v2.show()

print("-" * 80)

## 겹쳐서 표시 -> barmode="overlay" + opacity
fig_hist_v3 = px.histogram(
    data_frame=df_tips,
    x="total_bill",
    color="time",
    barmode="overlay",
    opacity=0.5
)
fig_hist_v3.update_traces(marker_line_color="#ffdb8c", marker_line_width=1)
fig_hist_v3.show()

print("-" * 80)

## 분리해서 표시 -> barmode="group"
fig_hist_v4 = px.histogram(
    data_frame=df_tips,
    x="total_bill",
    color="time",
    barmode="group"
)
fig_hist_v4.update_traces(marker_line_color="#fff07f", marker_line_width=1)
fig_hist_v4.show()

# 수평 히스토그램

## 시각화 목표: total_bill 금액 구간별 누적 빈도수 비교
## 수평형 -> x=None, y가 수치형 컬럼
fig_hist_h1 = px.histogram(
    data_frame=df_tips,
    x=None,
    y="total_bill"
)
fig_hist_h1.update_traces(marker_line_color="#ff8080", marker_line_width=1)
fig_hist_h1.show()

print("-" * 80)

## color="time" 첨가
fig_hist_h2 = px.histogram(
    data_frame=df_tips,
    y="total_bill",
    color="time"
)
fig_hist_h2.update_traces(marker_line_color="#ff8080", marker_line_width=1)
fig_hist_h2.show()

print("-" * 80)

## 겹쳐서 표시 -> barmode="overlay" + opacity
fig_hist_h3 = px.histogram(
    data_frame=df_tips,
    y="total_bill",
    color="time",
    barmode="overlay",
    opacity=0.5
)
fig_hist_h3.update_traces(marker_line_color="#ff8080", marker_line_width=1)
fig_hist_h3.show()

print("-" * 80)

## 분리해서 표시 -> barmode="group"
fig_hist_h4 = px.histogram(
    data_frame=df_tips,
    y="total_bill",
    color="time",
    barmode="group"
)
fig_hist_h4.update_traces(marker_line_color="#ff8080", marker_line_width=1)
fig_hist_h4.show()

# 수직 박스플롯(boxplot)

## 시각화 목표: 요일별 tip의 분포 비교
## 수직형 -> x가 범주형 컬럼, y가 수치형 컬럼
fig_box_v1 = px.box(
    data_frame=df_tips,
    x="day",
    y="tip",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    color="day"
)
fig_box_v1.show()

print("-" * 80)

## color="sex" 추가 -> 요일별, 손님의 성별 tip의 분포 비교
fig_box_v2 = px.box(
    data_frame=df_tips,
    x="day",
    y="tip",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    color="sex"
)
fig_box_v2.show()

# 수평 박스플롯(boxplot)

## 수평형 -> x가 수치형 컬럼, y가 범주형 컬럼
fig_box_h1 = px.box(
    data_frame=df_tips,
    x="tip",
    y="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    color="day"
)
fig_box_h1.show()

print("-" * 80)

## color="sex" 추가
fig_box_h2 = px.box(
    data_frame=df_tips,
    x="tip",
    y="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    color="sex"
)
fig_box_h2.show()

# 산점도 그래프

## 시각화 목표: 요금 총합과 팁의 관계(상관 관계)를 점의 분포로 표현하기
fig_scatter1 = px.scatter(
    data_frame=df_tips,
    x="total_bill",
    y="tip"
)
fig_scatter1.show()

print("-" * 80)

## color="time" -> 식사 시간별로 분할 후 요금의 총합과 팁의 관계 분석
fig_scatter2 = px.scatter(
    data_frame=df_tips,
    x="total_bill",
    y="tip",
    color="time"
)
fig_scatter2.show()

# heatmap 그래프

## 상관 분석 실행 -> 상관 행렬(DataFrame) 생성 -> df.corr()
df_corr = df_tips.corr(numeric_only=True)
print(f"상관 분석의 결과: \n{df_corr}")

print("-" * 80)

## 그래프 생성 및 출력 -> img에 상관 행렬 전달
fig_heatmap = px.imshow(
    img=df_corr,
    text_auto=".2f",
    color_continuous_scale="Inferno"
)
fig_heatmap.show()