"""TIL: Pydantic BaseModel로 상태 정의하기 (2026-11-20) — 개념 설명은 README.md 참고"""

from typing import Annotated, TypedDict
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import add_messages, StateGraph, END


# 1. Pydantic BaseModel 연습
## BaseModel을 상속하면 TypedDict와 달리 "진짜 새로운 자료형"이 만들어짐
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool


## 객체 생성
user = User(id=2, name="짱구", email="tt@example.com", is_active=False)

print(f"user: {user}")
## TypedDict는 <class 'dict'>였지만 BaseModel은 <class '__main__.User'>로 나옴
print(type(user))

## 각 항목의 값 추출 -> 점(.)으로 접근
id_data = user.id
name_data = user.name
email_data = user.email

print(f"id: {id_data}")
print(f"name: {name_data}")
print(f"email: {email_data}")

## 딕셔너리로 변환 -> 전용 함수 model_dump()
user_dict = user.model_dump()

print(f"딕셔너리 변환: \n{user_dict}")
print(f"딕셔너리 변환 결과 자료형 확인: {type(user_dict)}")

## 딕셔너리로 변환한 뒤에는 get()으로 접근
id_data = user_dict.get("id")
name_data = user_dict.get("name")
email_data = user_dict.get("email")

print(f"id: {id_data}")
print(f"name: {name_data}")
print(f"email: {email_data}")


# 2. 유효성 검사 비교
## 같은 구조를 TypedDict로도 만들어 잘못된 자료형을 넣어봄
class Customer(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool


## name은 str로 선언했는데 리스트를 넣음
## TypedDict -> 아무 일도 일어나지 않고 그대로 저장됨
customer = Customer(id=1, name=["수지"], email="rr@example.com", is_active=True)

print(f"customer: {customer}")

## BaseModel -> ValidationError 발생
## "Input should be a valid string [type=string_type, input_value=['수지'], input_type=list]"
# user1 = User(id=2, name=["수지"], email="rr@example.com", is_active=False)


# 3. LangGraph 상태 정의
## Field()로 기본값과 설명을 함께 달 수 있음
class AgentState(BaseModel):
    ## 대화 메시지 누적 구조 생성
    ## default_factory=list -> 객체를 만들 때마다 "새 빈 리스트"를 만들어 기본값으로 씀
    messages: Annotated[list[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="대화 이력 목록 (역할, 내용 포함)",
    )
    ## 도구 실행 결과 텍스트 저장
    tool_output: str | None = Field(
        ### 기본값
        default=None,
        ### 이 항목에 대한 설명
        description="도구 실행의 결과",
    )


# 4. 노드 함수 정의
## 상태가 BaseModel이므로 값을 꺼낼 때 state["messages"]가 아니라 state.messages로 접근함
## 반환은 여전히 딕셔너리이고, LangGraph가 그 딕셔너리를 상태 자료형으로 변환해 반영함


## 4-1. LLM 호출 노드
def call_llm(state: AgentState) -> dict:
    print("---LLM 호출 노드 실행---")
    print("-" * 80)

    ## 상태를 통째로 출력해보면 messages=[...] tool_output=None 형태로 찍힘
    print(f"state: {state}")
    print("-" * 80)

    ## 대화 히스토리 추출 -> 점으로 접근
    messages = state.messages

    ## 마지막 메시지가 HumanMessage인지 확인 후 content 값 가져오기
    if messages and isinstance(messages[-1], HumanMessage):
        last_user_message = messages[-1].content
    else:
        last_user_message = ""

    print(f"사용자 입력: {last_user_message}")
    print("-" * 80)

    ## 실제로는 LLM이 도구 사용 여부를 판단함. 여기서는 AIMessage를 직접 만들어 반환
    return {"messages": [AIMessage(content="도구 사용을 요청합니다.")]}


## 4-2. 도구 실행 노드
def call_tool(state: AgentState) -> dict:
    print("---도구 노드 실행---")
    print("-" * 80)

    ## 도구 실행을 시뮬레이션
    print("도구 실행 중...")
    tool_result = "도구 실행 완료"

    return {
        "messages": [ToolMessage(content=tool_result, tool_call_id="search_tool_call_id_123")],
        "tool_output": tool_result,
    }


## 4-3. 결과 요약 노드
def summarize_result(state: AgentState) -> dict:
    print("---결과 요약 노드 실행---")
    print("-" * 80)

    ## 상태에서 도구 실행 결과 추출 -> 점으로 접근
    tool_result = state.tool_output

    ## 실제로는 LLM이 요약함
    summary = f"도구 실행 결과 '{tool_result}'를 요약했습니다."

    return {"messages": [AIMessage(content=summary)]}


# 5. 그래프 구성
graph = StateGraph(AgentState)

## 노드 추가 -> add_node("이름", 함수 이름)
graph.add_node("call_llm_node", call_llm)
graph.add_node("call_tool_node", call_tool)
graph.add_node("summarize_node", summarize_result)

## 시작점 설정
graph.set_entry_point("call_llm_node")

## 엣지 추가
## LLM 실행 후 도구 호출
graph.add_edge("call_llm_node", "call_tool_node")

## 도구 사용 후 결과 요약
graph.add_edge("call_tool_node", "summarize_node")

## 결과 요약 후 종료
graph.add_edge("summarize_node", END)


# 6. 그래프 컴파일
agent = graph.compile()


# 7. 실행 및 결과 확인
print("Pydantic BaseModel 기반 에이전트 실행")
print("-" * 80)

user_question = "nvidia 2026년도 2분기 매출액은?"

## 초기 상태를 딕셔너리가 아니라 AgentState 객체로 만듦
initial_state = AgentState(messages=[HumanMessage(content=user_question)])

## 입력은 객체였지만 결과로 돌아오는 최종 상태는 딕셔너리임
final_state = agent.invoke(initial_state)

print(f"최종 상태: \n{final_state}")
print("-" * 80)
print(f"최종 상태 메시지: {final_state['messages']}")
print("-" * 80)
print(f"최종 LLM 출력: {final_state['messages'][-1].content}")
