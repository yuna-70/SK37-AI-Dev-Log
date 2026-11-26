"""TIL: 조건부 분기·비동기·체크포인팅을 합친 RAG 챗봇 (2026-11-26) — 개념 설명은 README.md 참고"""

import os
import asyncio
from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langgraph.graph import add_messages, StateGraph, END
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver


# 1. 환경 설정
file_path = ".env"
output = load_dotenv(file_path, override=True)

print(output)

llm = ChatOpenAI(model="gpt-5-nano")


# 2. RAG 시스템 기반 설정
csv_path = "faq_manual.csv"

loader = CSVLoader(
    file_path=csv_path,
    encoding="utf-8",
    content_columns=["question", "answer"],
)

docs = loader.load()

print(f"로드된 총 문서 수: {len(docs)}")

model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)

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

retriever = vectorstore.as_retriever(search_kwargs={"k": 1})


# 3. 에이전트별 전용 체인 생성

## 3-1. 의도 분류 체인
## 이전 대화 맥락과 최신 질문을 함께 보고 매뉴얼 검색이 필요한지 판별
## chat_history를 넣는 이유: "그건 어떻게 되나요?" 같은 후속 질문도 매뉴얼 문의일 수 있기 때문
classifier_system_prompt = """
당신은 온라인 교육 플랫폼 '코드크래프터스 아카데미'의 고객 문의 분류 전문가입니다.
이전 대화 기록(chat history)과 최신 사용자 질문을 함께 고려하여,
사내 고객 응대 매뉴얼(수강 신청, 회원가입, 환불 규정, 결제 수단, 강의 자료, 수료증 등) 조회가 필요한지 판단하세요.

- 플랫폼 이용, 강좌 정책, 환불, 결제, 수료증 등 회사 매뉴얼 확인이 필요한 문의(이전 매뉴얼 대화의 후속 질문 포함): 'RAG'
- 단순 인사말, 감사 표현, 일반 프로그래밍 상식/문법 질문 등 사내 매뉴얼이 필요 없는 대화: 'NO_RAG'

반드시 'RAG' 또는 'NO_RAG' 단어 하나만 정확하게 출력하세요. 다른 설명이나 공백은 일체 포함하지 마세요.
"""

classifier_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", classifier_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

classifier_chain = classifier_prompt | llm | StrOutputParser()


## 3-2. 질문 재구성 체인
rephrase_system_prompt = """
주어진 채팅 기록(chat history)과 최신 사용자 질문이 있을 때,
이 질문이 채팅 기록의 맥락을 참조하고 있다면 모호한 질문(예: "그거 전액 다 받으려면 조건이 뭐야?"),
채팅 기록 없이도 이해할 수 있는 명확한 질문(예: 수강 신청한 강의를 전액 환불 받으려면 조건이 뭐야?)으로 다시 작성하세요.
질문에 답하지 말고, 오직 질문을 재구성하거나 그대로 반환하기만 하세요.
"""

rephrase_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", rephrase_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

rephrase_chain = rephrase_prompt | llm | StrOutputParser()


## 3-3. 답변 생성 체인 두 개
## 검색 결과가 있을 때와 없을 때 프롬프트가 완전히 달라서 체인 자체를 나눔

### 1) RAG 기반 답변 체인
rag_qa_system_prompt = """
당신은 코드크래프터스 아카데미의 친절한 고객 지원 담당자입니다.
아래 제공된 [매뉴얼 내용]과 이전 대화 맥락을 바탕으로 고객의 질문에 정중하고 명확하게 답변해 주세요.
매뉴얼에 명시된 내용을 왜곡하지 말고 사실에 기반하여 친절하게 안내하세요.

[매뉴얼 내용]
{context}
"""

rag_qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rag_qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

## 출력 파서를 생략 -> 결과가 AIMessage 그대로라 상태에 바로 넣을 수 있음
rag_qa_chain = rag_qa_prompt | llm


### 2) 일반 대화용 답변 체인
general_qa_system_prompt = """
당신은 친절하고 명쾌한 답변을 하는 AI 비서입니다.
이전 대화 맥락을 기억하며 사용자의 질문이나 인사에 자연스럽고 유익하게 답변해 주세요.
"""

general_qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", general_qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

general_qa_chain = general_qa_prompt | llm


# 4. 그래프 상태 정의
class AgentState(BaseModel):
    ## 대화 내역 누적 항목
    messages: Annotated[list[BaseMessage], add_messages] = []
    ## 매뉴얼 검색(RAG) 필요 여부 저장
    needs_rag: bool = False
    ## 검색된 매뉴얼 내용 저장
    context: str = ""


# 5. 그래프 노드 함수 정의 (비동기 처리 방식)


## 5-1. 질문 의도 분류 노드
async def classifier_node(state: AgentState) -> dict:
    print("[Node 1: 질문 의도 분류] 실행 중...")

    latest_question = state.messages[-1].content
    chat_history = state.messages[:-1]

    decision = await classifier_chain.ainvoke(
        {
            "chat_history": chat_history,
            "input": latest_question,
        }
    )

    ## 앞뒤 공백 제거 후 대문자로 통일 -> 비교 실패 가능성을 줄임
    decision1 = decision.strip().upper()

    ## 단답형 응답 문자열 -> 불리언 변환
    needs_rag = decision1 == "RAG"

    print(f"LLM 판단 결과: {decision} (RAG 검색 필요 여부: {needs_rag})")
    print("-" * 80)

    return {"needs_rag": needs_rag}


## 5-2. 검색 노드
## 질문 재구성이 별도 노드가 아니라 이 안에 들어 있음
## 검색을 안 하는 질문에는 재구성도 필요 없기 때문
async def retriever_node(state: AgentState) -> dict:
    print("[Node 2: 사내 매뉴얼 검색 (RAG) 실행 중...]")
    print("-" * 80)

    latest_question = state.messages[-1].content
    chat_history = state.messages[:-1]

    ## 이전 대화 기록이 있을 때만 재구성 체인 실행
    if chat_history:
        query = await rephrase_chain.ainvoke(
            {
                "chat_history": chat_history,
                "input": latest_question,
            }
        )
        print(f"[결과] 재구성된 검색 쿼리: {query}")

    else:
        ## 첫 질문이면 재구성할 맥락이 없음
        query = latest_question

    ## 재구성된 질문으로 검색
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


## 5-3. 최종 답변 생성 노드
async def answer_node(state: AgentState) -> dict:
    print("[Node 3: 최종 답변 작성] 실행 중...")
    print("-" * 80)

    latest_question = state.messages[-1].content
    chat_history = state.messages[:-1]

    ## 상태에서 답변의 근거 추출
    context_text = state.context

    ## 검색을 거쳐왔는지에 따라 전용 답변 체인을 선택
    ## needs_rag만 보지 않고 context까지 함께 확인 -> 검색이 빈 결과를 돌려준 경우를 걸러냄
    if state.needs_rag and state.context:
        response = await rag_qa_chain.ainvoke(
            {
                "context": context_text,
                "chat_history": chat_history,
                "input": latest_question,
            }
        )

    else:
        response = await general_qa_chain.ainvoke(
            {
                "chat_history": chat_history,
                "input": latest_question,
            }
        )

    ## 대괄호로 감싼 리스트임에 주의
    ## 중괄호로 쓰면 집합(set)이 되고, AIMessage는 해시가 안 되어 TypeError가 남
    return {"messages": [response]}


# 6. 라우팅 함수 정의
## 상태의 needs_rag 값을 확인해 다음 이동 경로를 문자열로 반환
def route_by_rag_need(state: AgentState) -> str:
    ## 문서 검색이 필요한 경우
    if state.needs_rag:
        return "retriever_node"

    ## 문서 검색이 불필요한 경우 -> 검색을 건너뛰고 답변으로 직행
    else:
        return "answer_node"


# 7. 그래프 구성
graph = StateGraph(AgentState)

## 노드 추가
graph.add_node("classifier_node", classifier_node)
graph.add_node("retriever_node", retriever_node)
graph.add_node("answer_node", answer_node)

## 시작점 설정
graph.set_entry_point("classifier_node")

## 조건부 엣지 연결
graph.add_conditional_edges(
    ## 출발 노드
    "classifier_node",
    ## 라우팅 함수
    route_by_rag_need,
    ## {라우팅 함수의 반환값: 실제 노드 이름} 대응표
    {
        "retriever_node": "retriever_node",
        "answer_node": "answer_node",
    },
)

## 일반 엣지 연결
graph.add_edge("retriever_node", "answer_node")
graph.add_edge("answer_node", END)


# 8. 챗봇 실행
print("안녕하세요! 코드크래프터스 아카데미 지원 챗봇입니다. 무엇이든 물어보세요! (종료하려면 'exit' 입력)")
print("-" * 80)

## 체크포인트를 저장할 SQLite 데이터베이스 파일 경로 설정
db_file = "conditional_agent.sqlite"


async def main():
    ## async with로 비동기 체크포인터 생성
    async with AsyncSqliteSaver.from_conn_string(db_file) as memory:
        ## 그래프와 체크포인터 연결
        agent = graph.compile(checkpointer=memory)

        ## 특정 사용자 구별을 위한 고정 thread_id 설정
        config = {"configurable": {"thread_id": "user-8888"}}

        print("[비동기 방식 챗봇 에이전트] 가동 중...")
        print("=" * 80)

        while True:
            try:
                user_input = input("사용자: ")

                ## 종료 조건
                if user_input.lower() == "exit":
                    print("챗봇을 안전하게 종료합니다.")
                    break

                ## 이번 턴의 질문만 넣음 -> 이전 대화는 체크포인터가 붙여줌
                initial_state = {"messages": [HumanMessage(content=user_input)]}

                final_state = await agent.ainvoke(initial_state, config=config)

                ## 가장 최신 메시지(AIMessage)에서 텍스트 추출
                ai_answer = final_state["messages"][-1].content

                print(f"AI 에이전트:\n{ai_answer}")
                print("-" * 80)

            except Exception as e:
                print(f"오류가 발생했습니다: {e}")


## 주피터 노트북에서는 await main()으로 바로 실행
if __name__ == "__main__":
    asyncio.run(main())
