"""TIL: Transformer self-attention 직접 구현 (2026-11-09) — 개념 설명은 README.md 참고"""

import math
import torch
import torch.nn.functional as F


# 1. 입력 준비: 단어 임베딩 행렬 생성
## "I love you" -> 토큰화 [I, love, you] -> 정수 인덱스 [250, 12000, 700]
## Embedding Layer를 거치면 (단어 수, d_model) 모양의 임베딩 행렬이 됨
d_model = 512
embedding_matrix_shape = (3, d_model)
embedding_matrix = torch.randn(embedding_matrix_shape)

print(f"임베딩 행렬 모양: {embedding_matrix.shape}")


# 2. 가중치 행렬 생성
## W_q, W_k, W_v를 따로 만들지 않고 (512, 512*3) 한 덩어리로 생성
## math.sqrt(d_model)로 나눠 초기 가중치가 너무 커지지 않게 조정
weights_matrix = torch.randn(d_model, d_model * 3) / math.sqrt(d_model)

print(f"가중치 행렬 모양: {weights_matrix.shape}")

## 슬라이싱으로 W_q, W_k, W_v 분리
W_q = weights_matrix[:, 0:512]
W_k = weights_matrix[:, 512:1024]
W_v = weights_matrix[:, 1024:]

print(f"W_q 모양: {W_q.shape}")
print(f"W_k 모양: {W_k.shape}")
print(f"W_v 모양: {W_v.shape}")


# 3. q, k, v 행렬 생성
## 임베딩 행렬과 가중치 행렬의 곱: (3, 512) x (512, 1536) = (3, 1536)
qkv = torch.matmul(embedding_matrix, weights_matrix)

print(f"qkv 행렬 모양: {qkv.shape}")

## 한 번의 행렬 곱으로 얻은 결과를 셋으로 잘라 사용
query = qkv[:, 0:512]
key = qkv[:, 512:1024]
value = qkv[:, 1024:]

print(f"query 모양: {query.shape}")
print(f"key 모양: {key.shape}")
print(f"value 모양: {value.shape}")


# 4. Scaled Dot-Product Attention
## 4-1. attention score: query와 key의 행렬 곱
### query와 key는 둘 다 (3, 512)라 그대로는 곱할 수 없음
### key를 전치하면 (3, 512) x (512, 3) = (3, 3) 모든 단어 쌍의 점수표
attention_score = torch.matmul(query, key.mT)

print(f"attention_score: \n{attention_score}")

## 4-2. scaling: 차원의 제곱근으로 나눠 값의 크기를 줄임
scaled_attention_score = attention_score / math.sqrt(d_model)

print(f"scaled_attention_score: \n{scaled_attention_score}")

## 4-3. attention weight: softmax로 0~1 사이 비율로 변환
### dim=-1을 지정해야 행 기준으로 합이 1이 됨 (생략하면 UserWarning 발생)
attention_weight = F.softmax(scaled_attention_score, dim=-1)

print(f"attention_weight: \n{attention_weight}")
print(f"각 행의 합: {attention_weight.sum(dim=-1)}")

## 4-4. attention output: 반영 비율과 value의 가중합
### (3, 3) x (3, 512) = (3, 512) 문맥이 반영된 임베딩 벡터
output = torch.matmul(attention_weight, value)

print(f"output 모양: {output.shape}")
print(f"output: \n{output}")