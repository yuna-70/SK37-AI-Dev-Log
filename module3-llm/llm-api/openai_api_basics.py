"""TIL: OpenAI API 기본 사용법 (2026-11-12) — 개념 설명은 README.md 참고"""

import json
from dotenv import load_dotenv
from openai import OpenAI


# 1. 환경 설정
## .env 파일의 내용을 환경 변수로 올림
## 반환값 True는 .env 파일을 찾았다는 뜻
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")

## OpenAI 서버와의 연결 통로 생성
## 인자를 넘기지 않아도 환경 변수 OPENAI_API_KEY를 자동으로 읽음
client = OpenAI()


# 2. Chat Completions API
## 채팅(질의응답) 기능을 제공하는 API
response = client.chat.completions.create(
    model="gpt-5-nano",
    ## 시스템 프롬프트(역할 부여)와 사용자 프롬프트(요청)를 나눠서 전달
    messages=[
        {"role": "system", "content": "너는 친절하고 정확한 답변을 하는 AI 비서야"},
        {"role": "user", "content": "최대 200 토큰 내에서 대규모 언어 모델에 대해서 알려줘"},
    ],
)

print(f"응답 확인: \n{response}")

## 생성된 답변 텍스트만 추출
response_text = response.choices[0].message.content

print(f"AI 답변: \n{response_text}")

## 토큰 사용량 확인 -> 요금의 근거
## completion_tokens에는 화면에 안 보이는 reasoning_tokens가 포함됨
print(f"사용량: {response.usage}")


# 3. Responses API
## 웹 검색 같은 도구(tool)를 붙일 수 있는 API
response = client.responses.create(
    model="gpt-5-nano",
    ## 웹 검색 도구 활성화
    tools=[{"type": "web_search_preview"}],
    ## 시스템 프롬프트는 instructions 매개변수로 전달
    instructions="당신은 리서치 전문가이며, 사용자 요청에 대해 친절하고 정확한 답변을 해야 한다",
    ## 사용자 프롬프트는 input 매개변수로 전달
    input="오늘 주요 글로벌 IT 및 AI 관련 핵심 뉴스를 3가지로 요약해 줘",
)

## Responses API는 output_text로 텍스트를 바로 꺼냄
text = response.output_text

print(f"응답 확인: \n{text}")


# 4. 스트리밍 방식
## 데이터가 생성되는 즉시 토큰 단위로 받아 처리
response = client.chat.completions.create(
    model="gpt-5-nano",
    messages=[
        {"role": "system", "content": "너는 친절하고 정확한 답변을 하는 AI 비서야"},
        {"role": "user", "content": "최대 300 토큰 내에서 대규모 언어 모델에 대해서 알려줘"},
    ],
    ## 스트리밍 모드 활성화
    stream=True,
)

## 조각(chunk)을 하나씩 처리
for chunk in response:
    ## 스트리밍은 message가 아니라 delta에 내용이 담김
    content = chunk.choices[0].delta.content
    ## 역할 정보만 담긴 첫 조각과 종료 조각은 content가 None이므로 걸러냄
    if content is not None:
        print(content, end="")


# 5. JSON 문자열을 파이썬 dict로 변환
## 5-1. JSON 문자열과 파이썬 dict의 차이
json_string = '{"name":"짱구", "age":25, "city":"Seoul"}'
python_dict = {"name": "짱구", "age": 25, "city": "Seoul"}

print(f"JSON 문자열: {json_string}")
print(f"파이썬 dict: {python_dict}")

## 5-2. 작은따옴표를 쓰면 JSON이 아님
not_json_string = "{'name':'짱구', 'age':25, 'city':'Seoul'}"

print(f"잘못된 JSON 문자열: {not_json_string}")

## 5-3. json.loads()로 변환
## JSON 문자열을 파이썬 dict로 바꿔야 키로 값을 꺼낼 수 있음
python_dict = json.loads(json_string)

print(f"변환 결과: {python_dict}")
print(f"키로 값 꺼내기: {python_dict['name']}")

## 작은따옴표 문자열을 넣으면 JSONDecodeError 발생
# python_dict = json.loads(not_json_string)
