"""TIL: RAG 체인을 노드로 감싼 싱글 에이전트 챗봇 (2026-11-23) — 개념 설명은 README.md 참고"""

import os
from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import add_messages, StateGraph, END


# 1. 환경 설정
## override=True -> 이미 설정된 환경 변수가 있어도 .env 값으로 덮어씀
file_path = ".env"
output = load_dotenv(file_path, override=True)

print(output)


# 2. RAG 시스템 기반 설정

## 2-1. 데이터 로드 및 변환
## CSVLoader는 행별로 Document를 생성함
file_path = "faq_manual.csv"

loader = CSVLoader(
    file_path=file_path,
    encoding="utf-8",
    ## 본문(page_content)에 포함할 컬럼 지정
    ## faq_id와 category는 검색 대상 문장이 아니므로 넣지 않음
    content_columns=["question", "answer"],
)

docs = loader.load()

print(f"로드된 총 문서 수: {len(docs)}개")
print("-" * 60)
print(f"[첫 번째 Document 본문(page_content)]\n{docs[0].page_content}")
print("-" * 60)
print(f"[첫 번째 Document 메타데이터(metadata)]\n{docs[0].metadata}")


## 2-2. 텍스트 임베딩 모델 생성
## text-embedding-3-small: 최대 8,192 토큰, 임베딩 크기 1,536차원
model_name = "text-embedding-3-small"

model = OpenAIEmbeddings(model=model_name)


## 2-3. 벡터 저장소 생성 또는 불러오기
chroma_path = "chroma_db_rag"

if os.path.exists(chroma_path) and os.listdir(chroma_path):
    vectorstore = Chroma(
        persist_directory=chroma_path,
        embedding_function=model,
    )
    print("벡터 저장소 불러오기 성공")

else:
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=model,
        persist_directory=chroma_path,
    )
    print("벡터 저장소 새로 생성 성공")


## 2-4. 검색 도구 생성
## FAQ는 한 행이 곧 완결된 답이라 k=1
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

## 검색 도구 단독 테스트
user_query = "환불은 어떻게?"
output = retriever.invoke(user_query)

print(f"검색 결과: \n{output}")


# 3. RAG 체인 생성

## 3-1. 프롬프트 생성
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
    messages=[
        ("system", system_prompt),
        ("human", user_prompt),
    ]
)

print(prompt)


## 3-2. LLM과 출력 파서 생성
llm = ChatOpenAI(model="gpt-5-nano")
output_parser = StrOutputParser()


## 3-3. 체인 구성
## 지금까지 만든 RAG 체인과 똑같음. 이 체인을 통째로 노드 하나에 넣을 것임
rag_chain = prompt | llm | output_parser


# 4. 그래프 상태 정의
## 이번 실습의 상태는 messages 한 칸뿐임
class AgentState(BaseModel):
    ## 상태 메시지 누적 구조 생성
    messages: Annotated[list[BaseMessage], add_messages] = []


# 5. 그래프 노드 함수 정의
## 사용자의 질문을 받아 벡터 저장소에서 답변의 근거를 검색하고,
## RAG 체인을 실행해 답변을 생성하는 노드
def rag_node(state: AgentState) -> dict:
    print(f"state: \n{state}")

    ## 대화 히스토리에서 최신 사용자 질문 추출
    question = state.messages[-1].content

    ## 검색기 실행 -> 유사도가 가장 높은 문서 1개 추출
    retrieved_docs = retriever.invoke(question)

    ## 추출된 Document에서 텍스트 추출
    context_text = retrieved_docs[0].page_content

    ## RAG 체인 실행 -> 답변 텍스트 생성
    ## 체인에 StrOutputParser가 붙어 있어 response는 이미 문자열임
    response = rag_chain.invoke(
        {
            "context": context_text,
            "question": question,
        }
    )

    return {"messages": [AIMessage(content=response)]}


# 6. 그래프 구성 및 컴파일
graph = StateGraph(AgentState)

## 노드 추가
graph.add_node("rag_node", rag_node)

## 시작점 설정
graph.set_entry_point("rag_node")

## 노드 실행 완료 후 워크플로우가 종료되도록 엣지 연결
graph.add_edge("rag_node", END)

## 컴파일
agent = graph.compile()


# 7. 싱글 에이전트 실행
print("안녕하세요! 코드크래프터스 아카데미 지원 챗봇입니다. 무엇이든 물어보세요! (종료하려면 'exit' 입력)")
print("-" * 80)

while True:
    try:
        user_input = input("질문: ")

        ## 종료 조건
        if user_input.lower() == "exit":
            print("챗봇을 종료합니다. 이용해 주셔서 감사합니다.")
            break

        ## 사용자 질문을 초기 상태로 변환
        ## 매 턴 새 상태를 만들기 때문에 이전 대화는 남지 않음
        initial_state = AgentState(messages=[HumanMessage(content=user_input)])

        ## agent 실행 -> 최종 상태는 딕셔너리로 돌아옴
        final_state = agent.invoke(initial_state)

        ## 최종 상태의 가장 최신 메시지(AIMessage)에서 텍스트 추출
        ai_response = final_state["messages"][-1].content

        print(f"[Chatbot Agent 응답] \n{ai_response}")
        print("-" * 80)

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
