"""TIL: SentenceTransformer로 문장 유사도 측정 (2026-11-11) — 개념 설명은 README.md 참고"""

from sentence_transformers import SentenceTransformer


# 1. 영어 문장 유사도
## 같은 뜻을 다르게 쓴 두 문장
en_sentences = [
    "What should I do to be a great scientist?",
    "How can I be a good scientist?",
]

## 모델 이름만 주면 토큰화와 임베딩이 자동 처리됨
model_name = "all-MiniLM-L12-v2"
model_eng = SentenceTransformer(model_name)

## encode(): 텍스트 -> 임베딩 벡터
## 리스트를 넣으면 (문장 수, 차원) 모양의 행렬이 나옴
en_embeddings = model_eng.encode(en_sentences)

print(f"영어 텍스트에 대한 임베딩의 결과(모양): {en_embeddings.shape}")

## similarity(): 코사인 유사도 전용 함수
en_sim = model_eng.similarity(en_embeddings, en_embeddings)

print(f"영어 문장 간의 코사인 유사도: \n{en_sim}")


# 2. 한글 문장 유사도
## 2-1. 비교할 문장 두 쌍 생성
### 같은 뜻이지만 조사와 어순이 다른 두 문장
ko_sentences1 = [
    "직원이 무단 퇴사를 했는데 손해 배상 청구할 수 있나요?",
    "무단 퇴사한 직원에 대한 손해 배상 청구가 가능한가요?",
]

### 서로 무관한 두 문장
ko_sentences2 = [
    "직원이 무단 퇴사를 했는데 손해 배상 청구할 수 있나요?",
    "오늘도 날씨가 매우 덥고 소나기가 내리는 등 동남아 날씨같아요.",
]

## 2-2. 다국어 모델로 측정
model_name = "paraphrase-multilingual-MiniLM-L12-v2"
model_multi = SentenceTransformer(model_name)

ko_embeddings1 = model_multi.encode(ko_sentences1)
ko_embeddings2 = model_multi.encode(ko_sentences2)

print(f"다국어 모델 임베딩의 모양: {ko_embeddings1.shape}")

ko_sim1 = model_multi.similarity(ko_embeddings1, ko_embeddings1)
ko_sim2 = model_multi.similarity(ko_embeddings2, ko_embeddings2)

print(f"[다국어] 매우 유사한 두 문장 간의 코사인 유사도: \n{ko_sim1}")
print("-" * 80)
print(f"[다국어] 서로 무관한 두 문장 간의 코사인 유사도: \n{ko_sim2}")

## 2-3. 한국어 전용 모델로 측정
model_name = "ddobokki/klue-roberta-base-nli-sts"
model_kor = SentenceTransformer(model_name)

ko_embeddings3 = model_kor.encode(ko_sentences1)
ko_embeddings4 = model_kor.encode(ko_sentences2)

print(f"한국어 전용 모델 임베딩의 모양: {ko_embeddings3.shape}")

ko_sim3 = model_kor.similarity(ko_embeddings3, ko_embeddings3)
ko_sim4 = model_kor.similarity(ko_embeddings4, ko_embeddings4)

print(f"[한국어] 매우 유사한 두 문장 간의 코사인 유사도: \n{ko_sim3}")
print("-" * 80)
print(f"[한국어] 서로 무관한 두 문장 간의 코사인 유사도: \n{ko_sim4}")


# 3. 언어가 달라도 뜻이 같으면 가까운가
## 같은 질문을 4개 언어로 작성
sentences = [
    "What should I do to be a great scientist?",
    "훌륭한 과학자가 되려면 어떻게 해야 할까요?",
    "怎样才能成为一名优秀的科学家？",
    "¿Qué debo hacer para convertirme en un gran científico?",
]

model_name = "intfloat/multilingual-e5-large-instruct"
model_multi1 = SentenceTransformer(model_name)

multi_embeddings = model_multi1.encode(sentences)

print(f"4개 언어 텍스트에 대한 임베딩의 결과(모양): {multi_embeddings.shape}")

multi_sim = model_multi1.similarity(multi_embeddings, multi_embeddings)

print(f"4개 언어 텍스트에 대한 코사인 유사도: \n{multi_sim}")