"""TIL: TypedDict로 상태를 정의하고 그래프 구성·실행하기 (2026-11-19) — 개념 설명은 README.md 참고"""

from typing import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import add_messages, StateGraph, END


# 1. TypedDict 연습
## TypedDict는 딕셔너리의 키 이름과 값의 자료형을 미리 적어두는 클래스임
class User(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool


## 딕셔너리를 만드는 네 가지 방식
### 방식1: {} 기호 이용
dict_data1 = {}
dict_data1["name"] = "김짱구"
dict_data1["age"] = 23

print(dict_data1)
print(type(dict_data1))

### 방식2: dict() 생성 함수 이용
dict_data2 = dict(name="김짱구", age=23)

print(dict_data2)
print(type(dict_data2))

### 방식3: 클래스를 타입 힌트로 지정
dict_data3: User = {
    "id": 1,
    "name": "짱구",
    "email": "test@example.com",
    "is_active": True,
}

print(dict_data3)
print(type(dict_data3))

### 방식4: 클래스를 dict 함수처럼 호출
dict_data4 = User(id=2, name="수지", email="test2@example.com", is_active=False)

print(dict_data4)
## 네 방식 모두 type()은 <class 'dict'>로 나옴. TypedDict는 자료형을 새로 만들지 않음
print(type(dict_data4))


# 2. LangGraph 상태 정의
## 상태(State)는 노드들이 함께 보고 고쳐 쓰는 공용 작업판임
##
## messages 항목
##   대화 메시지: HumanMessage, AIMessage, ToolMessage
##   대화 흐름: 사용자 질문 -> LLM 답변(도구 호출 요청) -> 도구 사용
##   목표: [HumanMessage] -> [HumanMessage, AIMessage] -> [HumanMessage, AIMessage, ToolMessage]
##   그냥 list[BaseMessage]로 두면 새 메시지가 기존 목록을 "대체"해버려 대화 기록이 사라짐
##
## Annotated
##   기존 타입 힌트에 부가 정보(함수, 설명 등)를 덧붙이는 도구
##   Annotated[기존 자료형, 함수, 설명글] 형태로 씀
##
## add_messages
##   기존 메시지 리스트와 새 메시지 리스트를 이어붙이는 함수
##   [HumanMessage] + [AIMessage] -> [HumanMessage, AIMessage]로 대화 기록을 누적함
class AgentState(TypedDict):
    ## 대화 메시지 누적 구조 생성
    messages: Annotated[list[BaseMessage], add_messages]
    ## 도구 실행 결과 텍스트 저장
    tool_output: str | None


# 3. 노드 함수 정의
## 노드 함수의 규칙
##   매개 변수의 자료형은 AgentState로 지정하고, 입력값으로 상태 전체를 받음
##   실행 결과를 딕셔너리로 반환하면 LangGraph가 그 내용을 상태에 반영함
##   반환 딕셔너리의 키는 상태에 정의된 이름과 정확히 같아야 함
##
## 진행 순서(가정)
##   사용자 요청 -> call_llm(도구 사용 요청) -> call_tool(도구 실행) -> summarize_result(결과 요약)


## 3-1. LLM 호출 노드
def call_llm(state: AgentState) -> dict:
    print("---LLM 호출 노드 실행---")
    print("-" * 80)

    ## 상태에서 대화 히스토리 추출
    messages = state["messages"]

    ## 1턴일 때: [HumanMessage]
    ## 2턴일 때: [HumanMessage, AIMessage, ToolMessage, HumanMessage]

    ## isinstance(): 변수가 특정 자료형인지 확인해 True / False를 반환
    ## 마지막 메시지가 사용자 질문일 때만 content를 꺼냄
    if messages and isinstance(messages[-1], HumanMessage):
        last_user_message = messages[-1].content
    else:
        last_user_message = ""

    print(f"사용자 입력: {last_user_message}")
    print("-" * 80)

    ## 실제로는 LLM이 사용자 입력을 분석해 도구 사용 여부를 판단함
    ## 여기서는 도구 사용을 지시한다고 가정하고 AIMessage를 직접 만들어 반환
    return {"messages": [AIMessage(content="도구 사용을 요청합니다.")]}


## 3-2. 도구 실행 노드
def call_tool(state: AgentState) -> dict:
    print("---도구 노드 실행---")
    print("-" * 80)

    ## 실제로는 검색 도구 등을 실행함. 여기서는 실행을 흉내만 냄
    print("도구 실행 중...")
    tool_result = "도구 실행 완료"

    ## 도구 실행 결과는 ToolMessage로 감싸 messages에 쌓고,
    ## 다음 노드가 쉽게 꺼내 쓰도록 tool_output에도 따로 담음
    return {
        "messages": [ToolMessage(content=tool_result, tool_call_id="search_tool_call_id_123")],
        "tool_output": tool_result,
    }


## 3-3. 결과 요약 노드
def summarize_result(state: AgentState) -> dict:
    print("---결과 요약 노드 실행---")
    print("-" * 80)

    ## 상태에서 도구 실행 결과 추출
    tool_result = state["tool_output"]

    ## 실제로는 LLM이 요약함
    summary = f"도구 실행 결과 '{tool_result}'를 요약했습니다."

    return {"messages": [AIMessage(content=summary)]}


# 4. 그래프 구성
## 사용자 요청 -> call_llm_node -> call_tool_node -> summarize_result -> 종료(1턴)

## 그래프 생성. 어떤 상태를 쓸지 클래스로 알려줌
graph = StateGraph(AgentState)

## 노드 추가 -> add_node("노드 이름", 실행할 함수)
graph.add_node("call_llm_node", call_llm)
graph.add_node("call_tool_node", call_tool)
graph.add_node("summarize_result", summarize_result)

## 시작점 설정 -> set_entry_point()
graph.set_entry_point("call_llm_node")

## 엣지 추가 -> add_edge("출발 노드", "도착 노드")
## LLM 실행 후 도구 호출
graph.add_edge("call_llm_node", "call_tool_node")

## 도구 사용 후 결과 요약
graph.add_edge("call_tool_node", "summarize_result")

## 결과 요약 후 종료. END는 LangGraph가 미리 만들어둔 종료 지점
graph.add_edge("summarize_result", END)


# 5. 그래프 컴파일
## compile(): 설계도를 실행 가능한 구조로 변환
agent = graph.compile()


# 6. 실행 및 결과 확인
print("=== TypedDict 기반 에이전트 실행 ===")

user_question = "nvidia 2026년도 2분기 매출액은?"

## 사용자 질문을 상태에 입력 가능한 형태로 감쌈. 키 이름은 상태에 정의한 messages와 같아야 함
initial_state = {"messages": [HumanMessage(content=user_question)]}

## 결과물 추적
##   HumanMessage(사용자 요청) -> AIMessage(도구 호출 요청) -> ToolMessage(도구 작동) -> AIMessage(요약 생성)
final_state = agent.invoke(initial_state)

print(f"\n최종 상태: \n{final_state}")
print("-" * 80)
print(f"최종 상태 메시지: {final_state['messages']}")
print("-" * 80)
print(f"최종 LLM 출력: {final_state['messages'][-1].content}")
