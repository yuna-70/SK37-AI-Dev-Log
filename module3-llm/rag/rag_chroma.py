"""TIL: Chroma로 벡터 저장소를 디스크에 영속화하기 (2026-11-17) — 개념 설명은 README.md 참고"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(output)


# 2. 데이터 로드 및 Document 자료형으로 변환
txt_file_path = "manual.txt"
loader = TextLoader(file_path=txt_file_path, encoding="utf-8")

documents = loader.load()

print(f"documents: {documents}")


# 3. 데이터 분할
## FAISS 실습에서 계산해둔 근거(가장 긴 QA 157자)를 그대로 사용
text_splitter = RecursiveCharacterTextSplitter(chunk_size=160, chunk_overlap=0)

docs = text_splitter.split_documents(documents=documents)

print(f"분할된 문서의 수: {len(docs)}")
print(f"분할된 첫 번째 문서: \n{docs[0]}")


# 4. 임베딩 모델 생성
model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)


# 5. 벡터 저장소 생성 또는 불러오기
## Chroma는 persist_directory에 지정한 폴더에 데이터를 파일로 저장함
## 저장 테이블
##   embedding_metadata: 원본 텍스트, 메타 데이터
##   embeddings_queue: 임베딩 벡터
chroma_path = "chroma_db"

## 이미 생성된 벡터 저장소가 있으면 불러오고, 없으면 새로 생성
## 폴더가 있는지(os.path.exists)와 그 안에 내용이 있는지(os.listdir)를 함께 확인
if os.path.exists(chroma_path) and os.listdir(chroma_path):
    vectorstore = Chroma(
        persist_directory=chroma_path,
        ### 저장할 때 썼던 임베딩 모델을 다시 등록해야 질문도 같은 방식으로 벡터화됨
        embedding_function=model,
    )

else:
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=model,
        persist_directory=chroma_path,
    )

## 저장 폴더 안에 실제로 무엇이 만들어졌는지 확인
## 결과: ['ceb347b3-...', 'chroma.sqlite3'] -> SQLite 파일과 벡터 인덱스 폴더
print(os.path.exists(chroma_path))
print(os.listdir(chroma_path))


# 6. 검색 도구 생성
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

## 검색 도구 단독 테스트
user_query = "환불은"
output = retriever.invoke(user_query)

print(f"검색 결과: \n{output}")


# 7. 프롬프트 생성
system_prompt = """
당신은 친절한 온라인 교육 플랫폼 직원입니다.
제공된 [컨텍스트]를 바탕으로 고객의 질문에 정중하게 답변해주세요.

[답변 규칙]
1. [컨텍스트]의 내용을 바탕으로 자연스럽게 답변을 재구성하거나 그대로 활용하세요.
2. 답변 시 '답변:'이라는 표현을 사용하지 마세요.
3. [컨텍스트]에 질문에 대한 정보가 없다면, '죄송하지만 문의하신 내용에 대해서는 아는 바가 없습니다.'라고 답변하세요.

[컨텍스트]
{context}
"""

user_prompt = "{question}"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", user_prompt),
    ]
)

print(prompt)


# 8. LLM과 출력 파서 생성
llm = ChatOpenAI(model="gpt-5-nano")
output_parser = StrOutputParser()


# 9. RAG 체인 생성
rag_chain = prompt | llm | output_parser


# 10. 챗봇 실행
print("안녕하세요! 고객 응대 챗봇입니다. 궁금한 점을 질문해주세요. (종료하려면 'exit' 입력)")
print("-" * 80)

while True:
    try:
        user_query = input("질문: ")

        ## 종료 조건
        if user_query.lower() == "exit":
            print("챗봇을 종료합니다. 이용해주셔서 감사합니다.")
            break

        ## 10-1. 검색
        retrieved_docs = retriever.invoke(user_query)
        print(f"사용자 질문과 가장 유사한 문서 리스트: \n{retrieved_docs}")

        print("-" * 80)

        ## 10-2. 근거 추출
        context_text = retrieved_docs[0].page_content
        print(f"답변의 근거: \n{context_text}")

        print("-" * 80)

        ## 10-3. 생성
        response = rag_chain.invoke(
            {
                "context": context_text,
                "question": user_query,
            }
        )
        print(f"chatbot 응답: \n{response}")

        print("-" * 80)

    except Exception as e:
        print(f"오류가 발행합니다: {e}")
