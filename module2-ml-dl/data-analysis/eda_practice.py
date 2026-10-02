"""TIL: 탐색적 데이터 분석(EDA) 연습 문제 8문제 (2026-10-02) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd
import plotly.express as px

# 파이썬 경고 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 데이터 불러오기
file_path = "tips.csv"
df_tips = pd.read_csv(file_path)

# 문제 1
# 데이터 정렬과 선 그래프(Line Plot)
# tip 컬럼을 기준으로 데이터를 내림차순으로 정렬한 뒤,
# px.line을 사용하여 tip과 total_bill의 관계를 나타내세요.
df_tip_sorted = df_tips.sort_values(by="tip", ascending=False)

fig1 = px.line(
    data_frame=df_tip_sorted,
    x="tip",
    y="total_bill"
)
fig1.show()

# 문제 2
# 그룹화 연산과 수직 막대 그래프(Bar Chart)
# 성별(sex)에 따른 tip의 평균값을 구하고, 이를 데이터프레임으로 변환(reset_index)한 뒤
# 수직 막대 그래프로 시각화하세요.
sex_mean = df_tips.groupby(by="sex")["tip"].mean()
df_sex_mean = sex_mean.reset_index()

fig2 = px.bar(
    data_frame=df_sex_mean,
    x="sex",
    y="tip"
)
fig2.show()

# 문제 3
# 카테고리 정렬과 수평 막대 그래프(Horizontal Bar Chart)
# 요일(day)별 total_bill의 평균값을 구하여 데이터프레임으로 만든 뒤,
# 수평 막대 그래프(orientation="h")로 시각화하세요.
# 조건: 요일의 순서를 ["Thur", "Fri", "Sat", "Sun"]으로 직접 지정(category_orders)하세요.
day_total_mean = df_tips.groupby(by="day")["total_bill"].mean()
df_day_total_mean = day_total_mean.reset_index()

fig3 = px.bar(
    data_frame=df_day_total_mean,
    x="total_bill",
    y="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]},
    orientation="h",
    color="day"
)
fig3.show()

# 문제 4
# 빈도 분석과 원 그래프(Pie Chart)
# 식사 시간대(time)별 데이터의 빈도 비율을 구하고,
# 이를 도넛 형태(hole=0.3)의 원 그래프로 시각화하세요.
# 조건: value_counts(normalize=True)를 사용하여 비율을 계산하세요.
df_time_ratio = df_tips["time"].value_counts(normalize=True).reset_index()

fig4 = px.pie(
    data_frame=df_time_ratio,
    names="time",
    values="proportion",
    hole=0.3
)
fig4.show()

# 문제 5
# 데이터 분포 분석과 히스토그램(Histogram)
# tip 금액의 구간별 빈도수를 히스토그램으로 나타내되,
# 흡연 여부(smoker)에 따라 막대의 색상이 구분되도록 설정하세요.

# 그룹별 색상 구분은 y가 아니라 color가 담당함
fig5 = px.histogram(
    data_frame=df_tips,
    x="tip",
    color="smoker"
)
fig5.show()

# 문제 6
# 상자 그림(Box Plot)을 통한 분포 비교
# 요일(day)별 total_bill의 분포를 상자 그림으로 시각화하세요.
# 조건: 요일 순서를 ["Thur", "Fri", "Sat", "Sun"]으로 정렬하고, 수평 방향으로 그래프를 생성하세요.
fig6 = px.box(
    data_frame=df_tips,
    x="total_bill",
    y="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]}
)
fig6.show()

# 문제 7
# 상관 관계 시각화(Scatter Plot)
# total_bill과 tip의 관계를 산점도로 나타내되,
# 성별(sex)에 따라 점의 색상이 다르게 표시되도록 설정하세요.
fig7 = px.scatter(
    data_frame=df_tips,
    x="total_bill",
    y="tip",
    color="sex"
)
fig7.show()

# 문제 8
# 상관 분석과 히트맵(Heatmap)
# 데이터프레임의 모든 수치형 컬럼 간 상관 계수를 계산하여 상관 행렬을 만들고,
# 이를 px.imshow를 사용하여 히트맵으로 시각화하세요.
# 조건: 상관 계수 수치가 그래프 위에 표시되도록(text_auto) 설정하세요.
df_corr = df_tips.corr(numeric_only=True)

fig8 = px.imshow(
    img=df_corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r"
)
fig8.show()