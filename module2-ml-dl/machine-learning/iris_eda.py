"""TIL: 붓꽃 데이터 EDA - 품종별 특성 분포 비교 (2026-10-12) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd
import plotly.express as px

# 데이터 불러오기
file_path = "iris_dataset.csv"
df_iris = pd.read_csv(file_path)
display(df_iris)

# 데이터 전처리

## 각 컬럼별 누락 데이터의 수 확인
num_nulls = df_iris.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

# 특성별 품종 간의 차이 시각화

## 정답 컬럼 -> 품종별 개수 확인 -> 정답의 분포(균형 또는 불균형) 확인
label_counts = df_iris["label"].value_counts()
print(f"붓꽃 데이터의 품종별 개수: \n{label_counts}")

## 컬럼 이름 추출 -> 그래프의 x축 지정에 사용
column_names = df_iris.columns
print(f"붓꽃 데이터의 컬럼 이름: \n{column_names}")

## 꽃받침의 길이와 품종 간의 차이 시각화

### 전체 분포
fig_sepal_len_all = px.histogram(
    data_frame=df_iris,
    x=column_names[0],
    nbins=30,
    title="꽃받침의 길이 분포"
)
#### 모든 막대에 일괄적으로 검은색 경계선 넣기
fig_sepal_len_all.update_traces(marker_line_color="black", marker_line_width=1)
fig_sepal_len_all.show()

### 품종별 분포 -> color로 품종 구분, barmode="overlay"로 겹쳐 그리기
fig_sepal_len_label = px.histogram(
    data_frame=df_iris,
    x=column_names[0],
    nbins=30,
    title="품종별 꽃받침의 길이 분포",
    color=column_names[-1],
    barmode="overlay",
    opacity=0.6
)
fig_sepal_len_label.show()

## 꽃받침의 너비와 품종 간의 차이 시각화
fig_sepal_wid_all = px.histogram(
    data_frame=df_iris,
    x=column_names[1],
    nbins=30,
    title="꽃받침의 너비 분포"
)
fig_sepal_wid_all.update_traces(marker_line_color="black", marker_line_width=1)
fig_sepal_wid_all.show()

fig_sepal_wid_label = px.histogram(
    data_frame=df_iris,
    x=column_names[1],
    nbins=30,
    title="품종별 꽃받침의 너비 분포",
    color=column_names[-1],
    barmode="overlay",
    opacity=0.6
)
fig_sepal_wid_label.show()

## 꽃잎의 길이와 품종 간의 차이 시각화
fig_petal_len_all = px.histogram(
    data_frame=df_iris,
    x=column_names[2],
    nbins=30,
    title="꽃잎의 길이 분포"
)
fig_petal_len_all.update_traces(marker_line_color="black", marker_line_width=1)
fig_petal_len_all.show()

fig_petal_len_label = px.histogram(
    data_frame=df_iris,
    x=column_names[2],
    nbins=30,
    title="품종별 꽃잎의 길이 분포",
    color=column_names[-1],
    barmode="overlay",
    opacity=0.6
)
fig_petal_len_label.show()

## 꽃잎의 너비와 품종 간의 차이 시각화
fig_petal_wid_all = px.histogram(
    data_frame=df_iris,
    x=column_names[3],
    nbins=30,
    title="꽃잎의 너비 분포"
)
fig_petal_wid_all.update_traces(marker_line_color="black", marker_line_width=1)
fig_petal_wid_all.show()

fig_petal_wid_label = px.histogram(
    data_frame=df_iris,
    x=column_names[3],
    nbins=30,
    title="품종별 꽃잎의 너비 분포",
    color=column_names[-1],
    barmode="overlay",
    opacity=0.6
)
fig_petal_wid_label.show()

## 꽃잎의 길이와 꽃잎의 너비 관계 시각화 -> scatter
fig_petal_scatter = px.scatter(
    data_frame=df_iris,
    x=column_names[2],
    y=column_names[3],
    title="꽃잎의 길이와 꽃잎의 너비 관계",
    color=column_names[-1]
)
fig_petal_scatter.show()