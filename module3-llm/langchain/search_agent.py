"""TIL: 외부 검색 도구와 ReAct 에이전트 구현 (2026-11-13) — 개념 설명은 README.md 참고"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent


# 1. 환경 설정
## TavilySearch를 쓰려면 .env에 TAVILY_API_KEY도 함께 있어야 함
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")


# 2. 외부 검색 도구 살펴보기
## 2-1. 도구 생성
search_tool = TavilySearch(max_results=3)

print(search_tool)

## 2-2. 도구의 이름과 설명 확인
### 이 설명(description)을 에이전트가 읽고 언제 이 도구를 쓸지 판단함
tool_name = search_tool.name
tool_description = search_tool.description

print(f"도구 이름: {tool_name}")
print(f"도구 설명: {tool_description}")

## 2-3. 도구를 직접 실행
### 에이전트 없이 쓰면 검색 쿼리를 사람이 직접 만들어 넣어야 함
query = "Tesla의 2026년 2분기 실적"
query_results = search_tool.invoke(query)

print(f"검색 결과: \n{query_results}")


# 3. AI 에이전트 생성
## 3-1. 에이전트가 사용할 도구 목록 작성
### search_depth="advanced": 더 깊이 탐색
search_tool = TavilySearch(max_results=3, search_depth="advanced")
tools = [search_tool]

print(f"도구 목록: {tools}")

## 3-2. LLM 생성
llm = ChatOpenAI(model="gpt-5-nano")

## 3-3. 시스템 프롬프트 생성
### 검색 결과에 근거해서만 답하도록 지시 -> 환각 억제
system_prompt = """
너는 웹 검색 도구를 적극 활용하여 사용자 질문에 정확하고 객관적인 답변을 제공하는 전문 AI 에이전트야.
전달받은 웹 검색 결과에 기반하여 환각(Hallucination) 없이 사실만을 정리해 답변해야 해.
그리고 답변은 반드시 한국어로 작성할 것
"""

## 3-4. ReAct 에이전트 생성
agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt,
)


# 4. AI 에이전트 실행
## 도구 사용 판단 -> 실행 -> 결과 관찰 -> 답변 생성까지 자동으로 반복됨
## 사용자 프롬프트는 messages 형식의 딕셔너리로 전달
response = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "2026년 생성형 AI 시장 트렌드 및 최신 AI 에이전트 프레임워크 동향을 간단하게 정리해 줘",
            }
        ]
    }
)

print(f"[에이전트 전체 응답]: \n{response}")

## 최종 답변만 추출
## messages 리스트에 중간 과정이 모두 쌓이므로 마지막 것이 최종 답변
text = response["messages"][-1].content

print(f"[최종 에이전트 답변]: \n{text}")
