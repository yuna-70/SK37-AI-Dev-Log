"""TIL: 문장 유사도 기반 챗봇 구현 (2026-11-11) — 개념 설명은 README.md 참고"""

import numpy as np
import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


# 1. 데이터 불러오기
file_path = "ChatBotData.csv"
df = pd.read_csv(file_path)

print(df)

## 질문(Q)과 답변(A)만 사용하므로 label 컬럼 삭제
df1 = df.drop(columns=["label"])

print(f"질문-답변 쌍: {len(df1)}개")


# 2. 예상 질문 임베딩
## 사전 학습된 한국어 문장 임베딩 모델
model_name = "jhgan/ko-sroberta-multitask"
model = SentenceTransformer(model_name)

## Q 컬럼을 리스트로 변환
sentences = df1["Q"].tolist()

## 질문 하나씩 임베딩 벡터 생성
embedding_list = []
for sentence in tqdm(sentences):
    embedding = model.encode(sentence)
    embedding_list.append(embedding)

print(f"생성된 임베딩 벡터의 개수: {len(embedding_list)}개")

## 임베딩을 컬럼으로 저장 -> 질문이 들어올 때마다 다시 계산하지 않아도 됨
df1["embedding"] = embedding_list

print(df1)


# 3. 코사인 유사도 함수 직접 구현
## 1차원 배열 두 개를 받아 코사인 유사도를 반환
def cosine_similarity_np(v1, v2):
    v1 = np.asarray(v1)
    v2 = np.asarray(v2)

    ### 분자: 두 벡터의 내적
    dot_product = np.dot(v1, v2)

    ### 분모: 두 벡터의 크기(L2 노름)의 곱
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)

    ### 0으로 나누는 것을 방지
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0

    return dot_product / (norm_v1 * norm_v2)


# 4. 챗봇 함수 정의
def chatbot(question):
    ## 사용자 질문을 임베딩 벡터로 변환
    user_embedding = model.encode(question)

    ## 사용자 질문과 모든 예상 질문 간의 코사인 유사도 계산
    similarity_list = []
    for embedding in df1["embedding"]:
        sim = cosine_similarity_np(user_embedding, embedding)
        similarity_list.append(sim)

    df1["similarity"] = similarity_list

    ## 유사도가 가장 큰 행의 인덱스를 추출
    idx = df1["similarity"].idxmax()

    ## 그 행의 답변을 반환
    answer = df1.loc[idx, "A"]
    return answer


# 5. 챗봇 실행
question = "여행가고 싶다"
answer = chatbot(question)

print(f"chatbot: {answer}")