"""TIL: SentenceTransformer로 영화 추천 재구현 (2026-11-11) — 개념 설명은 README.md 참고"""

import pandas as pd
from sentence_transformers import SentenceTransformer


# 1. 데이터 불러오기
file_path = "movies_metadata.csv"
df = pd.read_csv(file_path)

print(f"원본 데이터: {df.shape}")


# 2. 전처리
## 줄거리와 제목만 사용
df1 = df[["overview", "title"]]

## 누락 데이터 확인 후 제거
num_nulls = df1.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

df2 = df1.dropna(ignore_index=True)
print(f"누락 제거 후: {len(df2)}편")

## 서로 비교하면 행렬 크기가 영화 수의 제곱이 되므로 1만 편으로 축소
df3 = df2[0:10000]


# 3. 줄거리 임베딩
## 11월 5일에는 CountVectorizer/TF-IDF를 썼고, 이번에는 문장 임베딩 모델을 사용
model_name = "all-MiniLM-L12-v2"
model = SentenceTransformer(model_name)

sentences = df3["overview"].tolist()
embeddings = model.encode(sentences)

print(f"영화 소개글 10000개에 대한 임베딩의 결과(모양): {embeddings.shape}")


# 4. 코사인 유사도 측정
## 모델 전용 함수로 모든 영화 쌍을 한 번에 계산
sim = model.similarity(embeddings, embeddings)

print(f"유사도 행렬의 모양: {sim.shape}")


# 5. 영화 추천 서비스 구현
## 5-1. 행과 열 인덱스를 영화 제목으로 지정 -> 제목으로 바로 조회 가능
index = df3["title"].values
columns = df3["title"].values
df_sim = pd.DataFrame(data=sim, index=index, columns=columns)

## 5-2. 특정 영화와 유사한 영화 추출
### 내림차순 1위는 언제나 자기 자신이므로 [1:n+1]로 자름
n = 10
top_n = df_sim["Toy Story"].sort_values(ascending=False)[1 : n + 1]

print(f"Toy Story와 줄거리가 가장 유사한 영화 top10: \n{top_n}")


# 6. 추천 함수 정의
def top_n_recommend(k, title):
    ## 사용자의 입력이 영화 제목에 있는 경우에만 실행
    if title in df_sim.columns:
        top_n = df_sim[title].sort_values(ascending=False)[1 : k + 1]
        return top_n
    else:
        print("존재하지 않는 영화 제목이오니, 확인 후 다시 입력을 해주세요")


# 7. 함수 실행
num = 10
name = "GoldenEye"
top_10 = top_n_recommend(k=num, title=name)

print(top_10)