# Module 3 - LLM (초거대언어모델)

> 2026년 11월 3일 시작

## 📚 학습 내용

**자연어 데이터 준비**
- 텍스트 전처리: 불용어 제거, 영어와 한글의 차이
- 토큰화: 문장 / 단어 / 서브워드(BPE, WordPiece) / 형태소
- 형태소 분석: konlpy Okt, MeCab
- 빈도수 분석과 시각화: Counter, WordCloud

**자연어 딥러닝**
- 임베딩: 희소 표현(BoW), CountVectorizer, TF-IDF
- 텍스트 유사도: 코사인 유사도
- RNN: 순차 데이터, BPTT, 기울기 소멸과 장기 의존성
- seq2seq, Transformer, BERT·GPT (예정)

**LLM** (예정)
- 프롬프트 엔지니어링
- 파인튜닝
- 멀티모달

## 📖 훈련 교재

- 파이썬 텍스트 마이닝 완벽 가이드
- RAG 시스템 구축을 위한 랭체인 실전 가이드
- 요즘 AI 에이전트 개발 (LLM, RAG, ADK, MCP, LangChain, A2A, LangGraph)
- 런팟(RunPod) 사용자 가이드

## 🚀 프로젝트

LLM 연동한 내외부 문서 기반 질의 응답 시스템

## 📂 폴더 구조

- `nlp/` — 토큰화, 형태소 분석, 임베딩, 코사인 유사도, RNN