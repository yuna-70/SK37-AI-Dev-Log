"""TIL: LangChain chain 기본과 감성 분석 애플리케이션 (2026-11-13) — 개념 설명은 README.md 참고"""

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")


# 2. chain의 세 가지 구성 요소
## 2-1. 첫 번째: 프롬프트
### ChatPromptTemplate의 from_messages()로 시스템·사용자 프롬프트를 한 번에 작성
### {topic} 자리의 값은 chain을 실행할 때 전달함
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 친절하고 정확한 답변을 하는 AI 비서야. 사용자의 질문에 100 토큰 이내로 간결하게 답변해야 해"),
        ("user", "{topic}에 대해서 설명해 줘"),
    ]
)

print(prompt)

## 2-2. 두 번째: LLM 모델
llm = ChatOpenAI(model="gpt-5-nano")

print(llm)

## 2-3. 세 번째: 출력 도구
### LLM 응답 객체에서 텍스트(문자열)만 꺼내주는 도구
output_parser = StrOutputParser()

print(output_parser)


# 3. chain 생성
## LCEL 방식: '|' 기호로 세 구성 요소를 순서대로 연결
chain = prompt | llm | output_parser

print(chain)


# 4. chain 실행
## invoke(): 프롬프트의 변수 값을 딕셔너리로 전달
output = chain.invoke({"topic": "양자 컴퓨터"})

print(f"chain 실행의 결과: \n{output}")


# 5. 적용: 고객 리뷰 감성 분석 chain
## 5-1. 프롬프트만 새로 작성
user_prompt = """
다음 한글로 작성된 <고객 리뷰>의 감성을 분석해서 판단 근거와 함께 결과를 긍정 또는 부정으로 제시하세요.
<고객 리뷰>
{review}
"""

review_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "당신은 한글로 작성된 고객 리뷰의 감성을 분석하는 경력 10년 이상의 뛰어난 분석가 입니다."),
        ("user", user_prompt),
    ]
)

print(review_prompt)

## 5-2. 나머지 두 구성 요소는 앞에서 만든 것을 그대로 재사용
review_chain = review_prompt | llm | output_parser

## 5-3. 분석할 고객 리뷰
customer_review = """
바지 밑위가 길고 제 허벅지는 터져나가서 상의를 넣어 입고 가만있을 때 정면모습이 쪼금 애매한 주름이 지네요
그래도 착용감은 편안하고 밝은 바지인데도 부한 느낌도 없어서 마음에 들어요
크림진이 하나도 없어서 고민고민하다 구매했는데 이정도면 만족입니다
다만 허리에 있는 가죽패치가 검정이라 세탁시 이염될까봐 무서운거랑 바지밑단 주름이 좀 자글자글하게 지는 단점은 있어요!
"""

## 5-4. 실행: 바뀌는 것은 프롬프트의 변수 값뿐
output = review_chain.invoke({"review": customer_review})

print(f"감성 분석 결과: \n{output}")
