"""TIL: 비지도 학습 - K-Means 붓꽃 군집화 (2026-10-16) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd
import plotly.express as px

# 데이터 불러오기

## 파일 경로 설정
file_path = "iris_dataset.csv"

## DataFrame 생성
df = pd.read_csv(file_path)
display(df)

## 꽃잎의 길이와 너비 관계 시각화
fig = px.scatter(
    data_frame=df,
    x="petal length (cm)",
    y="petal width (cm)",
    color="label",
    title="품종별 꽃잎의 길이와 너비 관계"
)
fig.show()

# 군집화에 사용할 데이터 생성

## fancy indexing -> 꽃잎의 길이, 꽃잎의 너비 추출
### 정답 컬럼(label)을 넣지 않는 이유: 비지도 학습이므로 정답 없이 군집을 찾음
data = df[["petal length (cm)", "petal width (cm)"]]
print("군집화에 사용할 데이터")
display(data)

# KMeans 모델을 이용한 군집화

## 2개의 군집으로 군집화

### 필요한 모델 클래스 임포트
from sklearn.cluster import KMeans

### 모델 생성
model1 = KMeans(n_clusters=2, random_state=0)

### fit_predict() 적용 -> 군집화 및 결과 확인
output1 = model1.fit_predict(data)
print(f"2개의 군집으로 군집화 결과: \n{output1}")

### 군집별 중심점 확인
print(f"군집별 중심점: \n{model1.cluster_centers_}")