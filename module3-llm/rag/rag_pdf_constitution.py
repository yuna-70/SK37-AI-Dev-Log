"""TIL: PDF 문서(대한민국헌법)로 만든 RAG 챗봇 (2026-11-17) — 개념 설명은 README.md 참고"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(output)


# 2. PDF 로드 및 Document 자료형으로 변환
## PyMuPDFLoader: PDF에서 텍스트를 추출해 Document로 변환
## TextLoader와 달리 페이지당 Document 1개가 생성됨 -> metadata에 page 번호가 들어감
pdf_file_path = "대한민국헌법(헌법)(제00010호)(19880225).pdf"
loader_pdf = PyMuPDFLoader(file_path=pdf_file_path)

documents_pdf = loader_pdf.load()

print(f"Document 페이지 수: {len(documents_pdf)}개")
print("-" * 80)
print(f"1페이지:\n{documents_pdf[0].page_content}")


# 3. 텍스트 분할
## 법률 문서는 조문 단위로 끊기는 편이 좋으므로 separators를 명시
## 헌법 조문은 QA 한 쌍보다 훨씬 길어서 chunk_size를 500으로 올림
## chunk_overlap=0 -> 조문이 중복되면 같은 내용이 여러 번 검색될 수 있음
text_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=500,
    chunk_overlap=0,
)

docs = text_splitter.split_documents(documents=documents_pdf)

print(f"세분화된 Document 개수: {len(docs)}개")
print("-" * 80)
print(f"세분화된 첫 번째 Document: \n{docs[0].page_content}")
print(f"세분화된 두 번째 Document: \n{docs[1].page_content}")


# 4. 임베딩 모델 생성
model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)


# 5. 벡터 저장소 생성 또는 불러오기
## manual.txt용 저장소와 폴더를 분리 -> 서로 다른 문서가 같은 저장소에 섞이지 않게 함
chroma_path = "chroma_db_constitution"

if os.path.exists(chroma_path) and os.listdir(chroma_path):
    vectorstore = Chroma(
        persist_directory=chroma_path,
        ### 이전에 사용했던 임베딩 모델을 등록
        embedding_function=model,
    )
    print("기존 벡터 저장소를 성공적으로 불러왔습니다.")

else:
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=model,
        persist_directory=chroma_path,
    )
    print("신규 벡터 저장소를 생성하고 저장했습니다.")


# 6. 검색 도구 생성
## k=2 -> 조문 하나로 답이 안 되는 질문이 많아서 2개를 가져옴
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

## 검색 도구 단독 테스트
user_query = "국회의원의 임기는 몇 년인가?"
output = retriever.invoke(user_query)

print(f"검색 결과: \n{output}")


# 7. 프롬프트 생성
## 1번 규칙: 조항 번호를 언급하게 해서 답변의 출처를 확인할 수 있게 함
## 3번 규칙: 근거가 없을 때 모른다고 답하게 하는 장치
system_prompt = """
당신은 신뢰할 수 있는 대한민국 헌법 전문 법률 Q&A 도우미입니다.
주어진 헌법 컨텍스트 정보를 바탕으로 사용자의 질문에 정확하고 공손하게 답변해주세요.

규칙:
1. 답변 시 관련된 헌법 조항(예: 제O조 제O항)이 [컨텍스트]에 명시되어 있다면 반드시 조항 번호를 언급해주세요.
2. [컨텍스트]의 내용에 근거해서만 답변해야 하며, 자의적인 해석이나 허위 정보를 만들지 마세요.
3. [컨텍스트]에 질문과 관련된 조문 내용이 전혀 없다면, "제시된 대한민국 헌법 문서에서 해당 내용을 찾을 수 없습니다."라고 답변해주세요.

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
print("안녕하세요! 대한민국헌법 Q&A 챗봇입니다. 헌법 조문이나 기본권 등에 대해 질문해주세요. (종료하려면 'exit' 입력)")
print("-" * 80)

while True:
    try:
        user_query = input("질문: ")

        ## 종료 조건
        if user_query.lower() == "exit":
            print("헌법 Q&A 챗봇을 종료합니다. 이용해주셔서 감사합니다.")
            break

        ## 10-1. 검색: 유사도가 높은 Document 2개를 리스트로 받음
        retrieved_docs = retriever.invoke(user_query)

        ## 10-2. 2개 문서의 텍스트를 하나의 문자열로 병합
        ### 빈 리스트 생성
        contents = []

        ### Document별 텍스트 추출
        for doc in retrieved_docs:
            contents.append(doc.page_content)

        ### join()으로 병합. 조문 사이를 "\n\n"로 띄워 서로 다른 조문임을 표시
        context_text = "\n\n".join(contents)

        print(f"[검색된 참조 조문 근거]:\n{context_text}")
        print("-" * 80)

        ## 10-3. 생성
        response = rag_chain.invoke(
            {
                "context": context_text,
                "question": user_query,
            }
        )

        print(f"chatbot 응답:\n{response}")
        print("-" * 80)

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
