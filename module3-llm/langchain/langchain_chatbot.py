"""TIL: LangChain으로 대화를 기억하는 챗봇 구현 (2026-11-13) — 개념 설명은 README.md 참고"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")


# 2. LLM 모델 생성
llm = ChatOpenAI(model="gpt-5-nano")


# 3. 대화형 프롬프트 정의
## LLM은 이전 대화를 기억하지 못하므로, 매 호출마다 대화 이력을 통째로 다시 보내야 함
## MessagesPlaceholder는 그 이력이 들어갈 자리를 프롬프트에 비워두는 역할
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 친절하고 전문적인 AI 비서야. 이전 대화 맥락을 정확하게 기억하여 사용자의 질문에 일관성 있게 답변해야 해"),
        MessagesPlaceholder(variable_name="chat_history"),
    ]
)

print(prompt)

## 출력 도구 생성
output_parser = StrOutputParser()


# 4. chain 생성
## LCEL 방식: '|' 기호로 연결
chatbot_chain = prompt | llm | output_parser

print(chatbot_chain)


# 5. 챗봇 실행
## 대화 이력을 저장할 빈 리스트 생성
chat_history = []

print("대화형 AI 챗봇이 시작되었습니다! \n")

## 종료 조건이 충족되기 전까지 계속 실행
while True:
    user_input = input("사용자 입력: ")

    ### 종료 조건 설정
    if user_input.lower() in ["q", "quit", "exit", "종료"]:
        break

    ### 사용자 입력을 HumanMessage로 감싸 이력에 추가
    ### 문자열 그대로가 아니라 누가 한 말인지 표시해야 LLM이 역할을 구분함
    chat_history.append(HumanMessage(content=user_input))

    ### chain 실행: 이력 전체를 넘김
    response = chatbot_chain.invoke({"chat_history": chat_history})

    print(f"AI 챗봇 답변: {response}\n")

    ### LLM의 답변도 AIMessage로 감싸 이력에 추가
    chat_history.append(AIMessage(content=response))
