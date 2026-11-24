"""TIL: 조건부 분기로 검색 여부를 가르는 에이전트 (2026-11-23) — 개념 설명은 README.md 참고"""

from typing import Annotated
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.graph import StateGraph, END, add_messages


# 1. 환경 설정
load_dotenv(".env")

llm = ChatOpenAI(model="gpt-5-nano")

## 검색 결과를 3개까지 가져옴
search_tool = TavilySearch(max_results=3)


# 2. 상태 정의
class AgentState(BaseModel):
    ## 상태 메시지 누적 구조 생성
    messages: Annotated[list[BaseMessage], add_messages] = []
    ## 웹 검색 필요 여부에 대한 표시 (True: 검색 필요, False: 불필요)
    needs_search: bool = False
    ## Tavily 검색 결과 저장
    search_results: str = ""


# 3. 노드 함수 정의


## 3-1. 사용자 질문 의도 분류 노드
## 사용자의 질문을 분석해 실시간 웹 검색이 필요한지를 단답형(SEARCH / NO_SEARCH)으로 생성
def classifier_node(state: AgentState) -> dict:
    print("[Node 1: 질문 의도 분류] 실행 중...")
    print("-" * 80)

    print(f"state: {state}")
    print("-" * 80)

    ## 대화 히스토리에서 사용자 질문 추출
    user_question = state.messages[-1].content

    print(f"[사용자 질문 원본]: {user_question}")
    print("-" * 80)

    ## LLM에게 단어 하나만 반환하도록 명확하게 지시
    ## 설명을 덧붙이면 아래 == 비교가 바로 깨지므로 금지 조항까지 넣음
    system_prompt = """
    당신은 사용자의 질문을 분석하는 전문가입니다.
    사용자의 질문에 답변하기 위해 실시간 웹 검색이 반드시 필요한지 판단하세요.

    - 최신 시사 뉴스, 실시간 정보, 특정 연도 실적(예: 2026년 실적) 등 최신 데이터 조회가 필요한 경우: 'SEARCH'
    - 일반 상식, 개념 설명, 프로그래밍 문법, 단순 인사말 등 모델 자체 지식으로 충분한 경우: 'NO_SEARCH'

    반드시 'SEARCH' 또는 'NO_SEARCH' 단어 하나만 정확하게 출력하세요. 다른 설명은 일체 포함하지 마세요.
    """

    messages = [
        ("system", system_prompt),
        ("user", f"질문: {user_question}"),
    ]

    response = llm.invoke(messages)

    print(f"llm의 답변: \n{response}")
    print("-" * 80)

    ## 앞뒤 공백 제거 후 대문자로 통일 -> 비교 실패 가능성을 줄임
    decision = response.content.strip().upper()

    ## 단답형 응답 문자열 -> 불리언 변환
    needs_search = decision == "SEARCH"

    print(f"LLM 판단 결과: {decision} (검색 필요 여부: {needs_search})")

    ## 바꿀 칸만 반환 -> 상태 업데이트
    return {"needs_search": needs_search}


## 3-2. Tavily 웹 검색 노드
## TavilySearch 도구를 실행해 최신 웹 정보를 수집하고 텍스트로 가공
def tavily_search_node(state: AgentState) -> dict:
    print("[Node 2: Tavily 웹 검색 도구 실행] 실행 중...")
    print("-" * 80)

    ## 대화 히스토리에서 사용자 최신 질문 추출
    query = state.messages[-1].content

    print(f"[검색 쿼리]: {query}")
    print("-" * 80)

    ## 검색 실패 시에도 그래프가 멈추지 않도록 기본값을 미리 만들어둠
    combined_results = "검색 결과가 없습니다."

    try:
        ## 실행 결과: 딕셔너리 -> 키 "results" -> 값은 딕셔너리의 리스트
        raw_results = search_tool.invoke({"query": query})

        ### 1. 결과에서 리스트 추출, 없으면 빈 리스트
        if isinstance(raw_results, dict):
            results = raw_results.get("results", [])
        else:
            results = []

        ### 2. 각 검색 결과에서 출처(url)와 본문(content) 추출
        context_parts = []

        for item in results:
            if isinstance(item, dict):
                url = item.get("url", "")
                content = item.get("content", "")
                context_parts.append(f"출처: {url}\n내용: {content}")
            else:
                context_parts.append(str(item))

        ### 3. 검색 결과 문자열들을 하나로 병합
        if context_parts:
            combined_results = "\n\n".join(context_parts)
            print(f"웹 검색 성공 (총 {len(context_parts)}개 문서 수집 완료)")
        else:
            print("검색 결과가 비어 있습니다.")

    except Exception as e:
        error_message = f"검색 중 오류 발생: {e}"
        print(error_message)
        combined_results = error_message

    ## 정제된 검색 결과 반환 -> 상태 업데이트
    return {"search_results": combined_results}


## 3-3. 최종 답변 생성 노드
## 검색 결과 유무에 따라 시스템 프롬프트를 동적으로 변경
def answer_node(state: AgentState) -> dict:
    print("[Node 3: 최종 답변 생성] 실행 중...")
    print("-" * 80)

    ## 검색 노드는 messages를 건드리지 않으므로 마지막 메시지는 여전히 사용자 질문임
    user_question = state.messages[-1].content

    ## 검색을 거쳐온 경우와 거치지 않은 경우에 맞춰 프롬프트를 다르게 구성
    if state.needs_search and state.search_results:
        ### 웹 검색 결과를 프롬프트에 반영
        system_prompt = f"""
        당신은 정확한 최신 정보를 제공하는 전문 AI 비서입니다.
        아래 제공된 [웹 검색 결과]를 바탕으로 사용자의 질문에 친절하고 명확하게 답변해 주세요.

        [웹 검색 결과]
        {state.search_results}
        """

    else:
        ### 일반적인 질문인 경우: 친절한 AI 비서로서의 지침만 부여
        system_prompt = """당신은 친절하고 똑똑한 AI 비서입니다. 사용자의 질문에
        명쾌하게 답변해 주세요."""

    messages = [
        ("system", system_prompt),
        ("user", user_question),
    ]

    ## llm.invoke()의 결과는 AIMessage 객체이므로 .content로 텍스트만 꺼냄
    response = llm.invoke(messages)

    print("-" * 80)

    return {"messages": [AIMessage(content=response.content)]}


# 4. 라우팅 함수 정의
## 상태의 needs_search 값을 읽고, 다음에 실행할 노드의 "이름"을 문자열로 반환
## 노드 함수와 달리 상태를 바꾸지 않고 경로만 결정함
def route_by_search_need(state: AgentState) -> str:
    if state.needs_search:
        print("[Router] 최신 정보 검색이 필요하므로 'search_node'로 이동합니다.")
        return "search_node"

    else:
        print("[Router] 검색이 불필요하므로 즉시 'answer_node'로 직행합니다.")
        return "answer_node"


# 5. 그래프 구성
graph = StateGraph(AgentState)

## 노드 추가
graph.add_node("classifier_node", classifier_node)
graph.add_node("search_node", tavily_search_node)
graph.add_node("answer_node", answer_node)

## 시작점 설정: 질문이 들어오면 항상 분류 노드부터 시작
graph.set_entry_point("classifier_node")

## 조건부 엣지 연결
## classifier_node 실행 후 route_by_search_need의 반환값에 따라 분기함
## 세 번째 인자는 {라우팅 함수의 반환값: 실제 노드 이름} 대응표
graph.add_conditional_edges(
    "classifier_node",
    route_by_search_need,
    {
        "search_node": "search_node",
        "answer_node": "answer_node",
    },
)

## 검색 노드 실행 후에는 최종 답변 생성 노드로 이동
graph.add_edge("search_node", "answer_node")

## 최종 답변 생성이 끝나면 워크플로우 종료
graph.add_edge("answer_node", END)


# 6. 그래프 컴파일
agent = graph.compile()


# 7. 실행 및 결과 확인

## 7-1. 테스트 1: 일반 지식 질문 (웹 검색 불필요 -> 즉시 답변 직행 경로 검증)
print("=" * 80)
print("테스트 1: 일반 지식 질문 (웹 검색 불필요 -> 즉시 답변 직행 경로 검증)")
print("=" * 80)

test_query1 = "파이썬에서 리스트와 튜플의 가장 핵심적인 차이점을 한 문장으로 설명해줘."

initial_state1 = AgentState(messages=[HumanMessage(content=test_query1)])

final_state1 = agent.invoke(initial_state1)
ai_response_text1 = final_state1["messages"][-1].content

print(f"[최종 AI 답변]: \n{ai_response_text1}")


## 7-2. 테스트 2: 실시간 최신 정보 질문 (웹 검색 필요 -> 검색 -> 답변 경로 검증)
print("=" * 80)
print("테스트 2: 실시간 최신 정보 질문 (웹 검색 필요 -> 검색 -> 답변 경로 검증)")
print("=" * 80)

test_query2 = "Nvidia 2026년 2분기 영업 실적 요약해 줘."

initial_state2 = AgentState(messages=[HumanMessage(content=test_query2)])

final_state2 = agent.invoke(initial_state2)
ai_response_text2 = final_state2["messages"][-1].content

print(f"[최종 AI 답변]:\n{ai_response_text2}")
