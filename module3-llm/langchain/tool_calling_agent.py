"""TIL: bind_tools로 에이전트 동작 직접 구현 (2026-11-16) — 개념 설명은 README.md 참고"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.output_parsers import StrOutputParser


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")


# 2. 도구 설정
search_tool = TavilySearch(max_results=3, search_depth="advanced")

## 에이전트(LLM)의 선택을 돕는 도구 목록
tools = [search_tool]

print(f"도구 목록: {tools}")


# 3. LLM 생성과 도구 바인딩
llm = ChatOpenAI(model="gpt-5-nano")

## bind_tools(): LLM에게 도구의 이름과 설명을 알려주고, 필요할 때 호출하도록 능력을 부여
## 도구를 실제로 실행해주지는 않고, "이 도구를 이런 인자로 부르고 싶다"는 요청만 만들어줌
llm_with_tools = llm.bind_tools(tools)

print(llm_with_tools)


# 4. 프롬프트 생성
## 언제 도구를 쓰고 언제 내부 지식으로 답할지를 시스템 프롬프트로 지시
system_prompt = """
너는 사용자의 질문에 정확하고 객관적인 답변을 제공하는 전문 AI 에이전트야.
1. 일반적인 대화나 이미 알고 있는 보편적인 지식만으로 충분히 답변할 수 있는 질문에는 웹 검색 도구를 호출하지 말고 네 내부 지식을 활용해 답변해.
2. 최신 정보, 실시간 트렌드, 또는 정확한 사실 확인이 필요한 질문에는 웹 검색 도구를 적극 호출하고, 검색 결과에 기반하여 환각(Hallucination) 없이
사실만을 정리해서 답변해.
그리고 모든 답변은 반드시 한국어로 작성해야 해.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

print(prompt)


# 5. 체인 두 개 생성
## 5-1. 1차 체인: 도구 호출 여부를 판단하는 용도
## 출력 파서를 붙이지 않음 -> AIMessage 객체 그대로 받아야 tool_calls를 확인할 수 있음
tool_calling_chain = prompt | llm_with_tools

## 5-2. 2차 체인: 검색 결과를 포함해 최종 텍스트 답변을 만드는 용도
## 도구가 붙지 않은 llm을 씀 -> 이 단계에서는 또 도구를 부르면 안 됨
output_parser = StrOutputParser()
final_answer_chain = prompt | llm | output_parser


# 6. 대화형 에이전트 실행
## 대화 이력을 저장할 빈 리스트 생성
messages = []

print("대화형 AI 에이전트가 시작되었습니다! \n")

while True:
    user_input = input("사용자: ")

    ## 종료 조건 설정
    if user_input.lower() in ["q", "exit", "quit", "종료"]:
        print("AI 에이전트: 대화를 종료합니다.")
        break

    ## 사용자 질문을 HumanMessage로 감싸 이력에 추가
    messages.append(HumanMessage(content=user_input))

    ## 6-1. 1차 체인 실행 -> 도구 필요 여부 판단
    ai_message = tool_calling_chain.invoke({"messages": messages})

    ## 도구를 부르기로 했으면 content는 비어 있고 tool_calls에 요청이 담김
    print(f"content: {ai_message.content}")
    print(f"tool_calls: {ai_message.tool_calls}")

    ## 1차 응답도 이력에 기록
    messages.append(ai_message)

    ## 6-2. 도구 호출 요청이 있으면 실행, 없으면 내부 지식으로 답변
    if ai_message.tool_calls:
        for tool_call in ai_message.tool_calls:
            ### LLM이 만들어준 검색 인자를 그대로 도구에 전달
            search_query = tool_call["args"]
            search_output = search_tool.invoke(search_query)

            ### 어느 호출에 대한 결과인지 짝을 맞추기 위한 고유 id
            tool_call_id = tool_call["id"]

            ### 도구 실행 결과를 ToolMessage로 감싸 이력에 추가
            messages.append(
                ToolMessage(
                    content=str(search_output),
                    tool_call_id=tool_call_id,
                )
            )

        ### 6-3. 2차 체인 실행 -> 검색 결과를 포함한 최종 답변 생성
        final_response = final_answer_chain.invoke({"messages": messages})

        print("[최종 LLM 답변]")
        print(final_response)

    else:
        print("[LLM 판단] 외부 검색 없이 내부 지식만으로 답변을 제공합니다.")
        print(ai_message.content)
