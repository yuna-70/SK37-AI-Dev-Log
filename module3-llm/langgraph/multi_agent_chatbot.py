"""TIL: 역할을 셋으로 나눈 멀티 에이전트 챗봇 (2026-11-24) — 개념 설명은 README.md 참고"""

import os
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


# 1. 환경 설정
file_path = ".env"
output = load_dotenv(file_path, override=True)

print(output)

## 두 체인이 함께 쓸 공통 LLM
llm = ChatOpenAI(model="gpt-5-nano")


# 2. RAG 시스템 기반 설정

## 2-1. 데이터 로드 및 변환
csv_path = "faq_manual.csv"

loader = CSVLoader(
    file_path=csv_path,
    encoding="utf-8",
    ## 본문(page_content)에 포함할 컬럼 지정
    content_columns=["question", "answer"],
)

docs = loader.load()

print(f"로드된 총 문서 수: {len(docs)}개")
print("-" * 60)
print(f"[첫 번째 Document 본문(page_content)]\n{docs[0].page_content}")
print("-" * 60)
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

## 검색 도구 단독 테스트
user_query = "환불은"
output = retriever.invoke(user_query)

print(f"검색 결과: \n{output}")


# 3. 에이전트별 전용 체인 생성

## 3-1. 질문 재구성 체인
## 맥락에 기대는 모호한 질문을 혼자서도 이해되는 질문으로 바꿈
## "질문에 답하지 말라"고 못 박지 않으면 LLM이 답을 해버림
rephrase_system_prompt = """
주어진 채팅 기록(chat history)과 최신 사용자 질문이 있을 때,
이 질문이 채팅 기록의 맥락을 참조하고 있다면 모호한 질문(예: "그거 전액 다 받으려면 조건이 뭐야?"),
채팅 기록 없이도 이해할 수 있는 명확한 질문(예: 수강 신청한 강의를 전액 환불 받으려면 조건이 뭐야?)으로 다시 작성하세요.
질문에 답하지 말고, 오직 질문을 재구성하거나 그대로 반환하기만 하세요.
"""

rephrase_prompt = ChatPromptTemplate.from_messages(
    messages=[
        ("system", rephrase_system_prompt),
        ## invoke 실행 시 대화 기록을 리스트로 받아 이 자리에 펼쳐 넣음
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

print(rephrase_prompt)

## 결과를 검색어로 쓸 것이므로 StrOutputParser로 문자열만 뽑음
rephrase_chain = rephrase_prompt | llm | StrOutputParser()


## 3-2. 답변 생성 체인
## 검색된 문서와 대화 맥락을 함께 보고 최종 답변을 작성
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
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

print(qa_prompt)

## 출력 파서를 붙이지 않음 -> 결과가 AIMessage 그대로라 상태에 바로 넣을 수 있음
qa_chain = qa_prompt | llm


# 4. 그래프 상태 정의
## 세 에이전트가 주고받을 칸을 모두 상태에 둠
class AgentState(BaseModel):
    ## 대화 내역 누적 항목
    messages: Annotated[list[BaseMessage], add_messages] = []
    ## 질문 재구성 에이전트가 만든 검색어
    rephrased_query: str = ""
    ## 검색 에이전트가 찾은 매뉴얼 내용
    context: str = ""


# 5. 그래프 노드 함수 정의
## 턴이 쌓이면 messages는 이렇게 늘어남
##   1턴: [HumanMessage]
##   2턴: [HumanMessage, AIMessage, HumanMessage]
##   3턴: [HumanMessage, AIMessage, HumanMessage, AIMessage, HumanMessage]


## 5-1. 질문 재구성 노드 (에이전트 1)
def rephrase_node(state: AgentState) -> dict:
    print("에이전트 1: 질문 맥락 분석 및 재구성")
    print("-" * 80)

    print(f"state: \n{state}")
    print("-" * 80)

    ## 맨 끝이 이번 턴의 사용자 질문
    latest_question = state.messages[-1].content

    ## 맨 끝을 뺀 나머지가 이전 대화 내역
    chat_history = state.messages[:-1]

    ## 첫 턴이면 이전 대화가 없으므로 재구성할 것도 없음 -> LLM 호출을 건너뜀
    if chat_history:
        query = rephrase_chain.invoke(
            {
                "chat_history": chat_history,
                "input": latest_question,
            }
        )

    else:
        query = latest_question

    print(f"[결과] 재구성된 쿼리: {query}")

    return {"rephrased_query": query}


## 5-2. 검색 노드 (에이전트 2)
def retriever_node(state: AgentState) -> dict:
    print("에이전트 2: 관련 매뉴얼 검색")

    ## 원본 질문이 아니라 재구성된 질문으로 검색함
    query = state.rephrased_query

    retrieved_docs = retriever.invoke(query)

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


## 5-3. 답변 생성 노드 (에이전트 3)
def answer_node(state: AgentState) -> dict:
    print("에이전트 3: 최종 답변 작성")
    print("-" * 80)

    latest_question = state.messages[-1].content
    chat_history = state.messages[:-1]

    ## 검색 노드가 상태에 넣어둔 답변의 근거
    context = state.context

    ## qa_chain에 출력 파서가 없으므로 response는 AIMessage 객체임
    response = qa_chain.invoke(
        {
            "context": context,
            "chat_history": chat_history,
            "input": latest_question,
        }
    )

    ## 이미 AIMessage이므로 다시 감싸지 않고 그대로 넣음
    return {"messages": [response]}


# 6. 그래프 구성 및 컴파일
graph = StateGraph(AgentState)

## 노드 추가
graph.add_node("rephrase_node", rephrase_node)
graph.add_node("retriever_node", retriever_node)
graph.add_node("answer_node", answer_node)

## 시작점 설정
graph.set_entry_point("rephrase_node")

## 엣지 추가 -> rephrase_node -> retriever_node -> answer_node -> END
graph.add_edge("rephrase_node", "retriever_node")
graph.add_edge("retriever_node", "answer_node")
graph.add_edge("answer_node", END)

## 컴파일
multi_agent = graph.compile()


# 7. 챗봇 실행
print("안녕하세요! 코드크래프터스 아카데미 지원 챗봇입니다. 무엇이든 물어보세요! (종료: exit)")
print("-" * 80)

## 한 번의 invoke가 END에 닿으면 상태는 사라짐
## 멀티턴 대화를 하려면 대화 기록을 while 바깥에 두고 계속 이어받아야 함
##   1턴 시작: {"messages": []}
##   2턴 시작: {"messages": [HumanMessage, AIMessage]}
##   3턴 시작: {"messages": [HumanMessage, AIMessage, HumanMessage, AIMessage]}
inputs = {"messages": []}

while True:
    try:
        user_input = input("사용자: ")

        ## 종료 조건
        if user_input.lower() == "exit":
            print("챗봇을 안전하게 종료합니다.")
            break

        ## 이번 턴의 질문을 기존 대화 기록 뒤에 덧붙임
        inputs["messages"].append(HumanMessage(content=user_input))

        ## agent 실행 -> 최종 상태는 딕셔너리로 돌아옴
        final_state = multi_agent.invoke(inputs)

        ## 가장 최신 메시지(AIMessage)에서 텍스트 추출
        ai_answer = final_state["messages"][-1].content

        print(f"AI 에이전트: \n{ai_answer}")
        print("-" * 80)

        ## 다음 턴에서 과거 대화를 기억하도록 최종 상태를 그대로 입력으로 넘김
        inputs = final_state

    except Exception as e:
        print(f"오류가 발생했습니다.: {e}")
