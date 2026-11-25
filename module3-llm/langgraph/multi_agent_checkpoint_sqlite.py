"""TIL: SQLite 체크포인터로 대화를 저장하는 멀티 에이전트 (2026-11-25) — 개념 설명은 README.md 참고"""

import os
import asyncio
from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END, add_messages
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


# 1. 환경 설정
file_path = ".env"
output = load_dotenv(file_path, override=True)

print(output)

## 매개 변수 이름은 소문자 model임
## 대문자 Model로 쓰면 LangChain이 모르는 설정으로 보고 model_kwargs에 넣어버림
llm = ChatOpenAI(model="gpt-5-nano")


# 2. RAG 시스템 기반 설정

## 2-1. 데이터 로드 및 변환
csv_path = "faq_manual.csv"

loader = CSVLoader(
    file_path=csv_path,
    encoding="utf-8",
    content_columns=["question", "answer"],
)

docs = loader.load()

print(f"로드된 총 문서 수: {len(docs)}개")
print("-" * 80)
print(f"[첫 번째 Document 본문(page_content)]\n{docs[0].page_content}")
print("-" * 80)
print(f"[첫 번째 Document 메타데이터(metadata)]\n{docs[0].metadata}")


## 2-2. 텍스트 임베딩 모델 생성
model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)


## 2-3. 벡터 저장소 생성 또는 불러오기
chroma_path = "chroma_db_multi"

if os.path.exists(chroma_path) and os.listdir(chroma_path):
    vectorstore = Chroma(
        persist_directory=chroma_path,
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


## 2-4. 검색 도구 생성
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})


# 3. 에이전트별 전용 체인 생성

## 3-1. 질문 재구성 체인
rephrase_system_prompt = """
주어진 채팅 기록(chat history)과 최신 사용자 질문이 있을 때,
이 질문이 채팅 기록의 맥락을 참조하고 있다면 모호한 질문(예: "그거 전액 다 받으려면 조건이 뭐야?"),
채팅 기록 없이도 이해할 수 있는 명확한 질문(예: 수강 신청한 강의를 전액 환불 받으려면 조건이 뭐야?)으로 다시 작성하세요.
질문에 답하지 말고, 오직 질문을 재구성하거나 그대로 반환하기만 하세요.
"""

rephrase_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rephrase_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

rephrase_chain = rephrase_prompt | llm | StrOutputParser()


## 3-2. 답변 생성 체인
qa_system_prompt = """
당신은 코드크래프터스 아카데미의 친절한 고객 지원 담당자입니다.
아래의 [Context] 정보를 사용하여 사용자의 질문에 답변하세요.
정보가 없다면 '죄송하지만 매뉴얼에서 정보를 찾을 수 없습니다'라고 답하세요.

[Context]
{context}
"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

## 출력 파서를 붙이지 않음 -> 결과가 AIMessage 그대로라 상태에 바로 넣을 수 있음
qa_chain = qa_prompt | llm


# 4. 그래프 상태 정의
class AgentState(BaseModel):
    ## 대화 내역 누적 항목
    messages: Annotated[list[BaseMessage], add_messages] = []
    ## 재구성된 질문 저장
    rephrased_query: str = ""
    ## 검색된 매뉴얼 내용 저장
    context: str = ""


# 5. 그래프 노드 함수 정의 (비동기 처리 방식)
## async def로 정의하면 LangGraph가 알아서 비동기로 실행함
## 체인 실행도 invoke가 아니라 await ... ainvoke()를 씀


## 5-1. 질문 재구성 노드
async def rephrase_node(state: AgentState) -> dict:
    print("에이전트 1: 질문 맥락 분석 및 재구성")
    print("-" * 80)

    ## 대화 히스토리에서 사용자 최신 질문 추출
    latest_question = state.messages[-1].content

    ## 최신 질문 이전의 대화 내역
    chat_history = state.messages[:-1]

    ## 이전 대화 기록이 있을 때만 재구성 체인 실행
    if chat_history:
        query = await rephrase_chain.ainvoke(
            {
                "chat_history": chat_history,
                "input": latest_question,
            }
        )

    else:
        ## 첫 질문이면 재구성할 맥락이 없음
        query = latest_question

    print(f"[결과] 재구성된 쿼리: {query}")

    return {"rephrased_query": query}


## 5-2. 검색 노드
async def retriever_node(state: AgentState) -> dict:
    print("에이전트 2: 관련 매뉴얼 검색")

    ## 상태에서 재구성된 질문 추출
    query = state.rephrased_query

    ## 검색 도구도 비동기로 실행
    retrieved_docs = await retriever.ainvoke(query)

    ## 검색된 문서 리스트를 순회하며 텍스트 추출
    contents = []

    for doc in retrieved_docs:
        text = doc.page_content
        contents.append(text)

    ## join()으로 "\n\n" 기준 연결
    context_text = "\n\n".join(contents)

    print(f"답변의 근거: \n{context_text}")
    print("-" * 80)

    return {"context": context_text}


## 5-3. 답변 생성 노드
async def answer_node(state: AgentState) -> dict:
    print("에이전트 3: 최종 답변 작성")
    print("-" * 80)

    latest_question = state.messages[-1].content
    chat_history = state.messages[:-1]

    ## 검색 노드가 상태에 넣어둔 답변의 근거
    context = state.context

    response = await qa_chain.ainvoke(
        {
            "context": context,
            "chat_history": chat_history,
            "input": latest_question,
        }
    )

    ## qa_chain에 출력 파서가 없어 response는 이미 AIMessage임
    return {"messages": [response]}


# 6. 그래프 구성
graph = StateGraph(AgentState)

## 노드 추가
graph.add_node("rephrase_node", rephrase_node)
graph.add_node("retriever_node", retriever_node)
graph.add_node("answer_node", answer_node)

## 시작점 설정
graph.set_entry_point("rephrase_node")

## 엣지 추가
graph.add_edge("rephrase_node", "retriever_node")
graph.add_edge("retriever_node", "answer_node")
graph.add_edge("answer_node", END)


# 7. 챗봇 실행
## 체크포인트를 저장할 SQLite 데이터베이스 파일명 설정
db_file = "multi_agent.sqlite"


async def main():
    ## async with로 비동기 체크포인터 생성
    ## 블록을 빠져나갈 때 연결을 알아서 닫아줌
    async with AsyncSqliteSaver.from_conn_string(db_file) as memory:
        ## 그래프 컴파일 -> 그래프와 체크포인터 연결
        ## 컴파일을 여기서 하는 이유는 체크포인터가 async with 안에서만 살아 있기 때문임
        multi_agent = graph.compile(checkpointer=memory)

        ## 특정 사용자를 구별하기 위한 thread_id 고정
        ## 같은 thread_id로 실행하면 이전 대화를 이어받고, 바꾸면 새 대화가 됨
        config = {"configurable": {"thread_id": "user-8888"}}

        print("[비동기 방식 멀티 에이전트] 가동 중... (종료: exit)")
        print("-" * 80)

        while True:
            try:
                user_input = input("사용자: ")

                ## 종료 조건
                if user_input.lower() == "exit":
                    print("챗봇을 안전하게 종료합니다.")
                    break

                ## 초기 상태에 이번 턴의 질문만 넣음
                ## 이전 대화는 체크포인터가 thread_id로 찾아 붙여줌
                initial_state = {"messages": [HumanMessage(content=user_input)]}

                ## agent 실행 -> config로 어느 대화인지 알려줌
                final_state = await multi_agent.ainvoke(initial_state, config=config)

                ## 가장 최신 메시지(AIMessage)에서 텍스트 추출
                ai_answer = final_state["messages"][-1].content

                print(f"AI 에이전트:\n{ai_answer}")
                print("-" * 80)

            except Exception as e:
                print(f"오류가 발생했습니다.: {e}")


## 주피터 노트북에서는 await main()으로 바로 실행
## .py 파일로 돌릴 때는 asyncio.run()으로 감싸야 함
if __name__ == "__main__":
    asyncio.run(main())
