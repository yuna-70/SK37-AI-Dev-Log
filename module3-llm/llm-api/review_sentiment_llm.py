"""TIL: OpenAI API로 고객 리뷰 감성 분석 (2026-11-12) — 개념 설명은 README.md 참고"""

import json
from dotenv import load_dotenv
from openai import OpenAI


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")

client = OpenAI()


# 2. 실행 함수 정의
def get_completion(prompt, model="gpt-5-nano"):
    response = client.chat.completions.create(
        model=model,
        ## 역할 부여: 감성 분석 전문가로 지정
        messages=[
            {
                "role": "system",
                "content": "너는 한글로 된 고객 리뷰에 대한 경력 10년 이상의 우수한 감성 분석 전문가야.",
            },
            {"role": "user", "content": prompt},
        ],
        ## 응답 형식: JSON 문자열
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


# 3. 분석할 고객 리뷰
## 긍정과 부정이 섞여 있는 리뷰
customer_review = """
바지 밑위가 길고 제 허벅지는 터져나가서 상의를 넣어 입고 가만있을 때 정면모습이 쪼금 애매한 주름이 지네요
그래도 착용감은 편안하고 밝은 바지인데도 부한 느낌도 없어서 마음에 들어요
크림진이 하나도 없어서 고민고민하다 구매했는데 이정도면 만족입니다
다만 허리에 있는 가죽패치가 검정이라 세탁시 이염될까봐 무서운거랑 바지밑단 주름이 좀 자글자글하게 지는 단점은 있어요!
"""


# 4. 감성 분석 (1) 결과만 받기
## 정답 예시를 JSON 문자열로 작성
## 파이썬 dict를 f-string에 그대로 넣으면 작은따옴표로 출력되어 JSON 형식과 달라짐
example = json.dumps({"감성 분석 결과": "긍정"}, ensure_ascii=False)

## 리뷰를 triple backticks로 감싸 지시문과 데이터를 구분
user_prompt1 = f"""
triple backticks로 처리된 한글 text를 분석해서 <정답 예시>처럼 긍정인지 부정인지를 JSON 형식으로 제시해 줘.

한글 text:
```{customer_review}```

<정답 예시>
{example}
"""

print(user_prompt1)

output1 = get_completion(prompt=user_prompt1)

print(f"LLM 출력: \n{output1}")


# 5. 감성 분석 (2) 판단 근거까지 받기
## 출력 형식을 자세히 지정 -> 키워드와 판단 이유를 함께 요구
example = """
{
    "감성 분석 결과": "긍정",
    "판단 근거 키워드": {
        "긍정": ["키워드1", "키워드2"],
        "부정": ["키워드1", "키워드2"]
    },
    "최종 판단의 이유": "부정적인 요소도 있지만, 만족이라는 강력한 긍정의 표현이 포함되어 있다."
}
"""

user_prompt2 = f"""
다음 <고객 리뷰>의 내용을 분석하여 긍정 또는 부정으로 감성 분류하고, 해당 분류의
판단 근거가 되는 핵심 키워드들을 추출한 후 <출력 형식>을 철저히 준수하여 결과를 제시하고,
긍정과 부정의 요소가 다 포함이 되어 있는 경우에는 긍정 또는 부정이라고 판단한 이유를 제시하시오.

<고객 리뷰>
{customer_review}

<출력 형식>
아래 JSON 형식을 엄격하게 준수하여 결과를 생성해야 합니다.
{example}
"""

print(user_prompt2)

output2 = get_completion(user_prompt2)

print(f"LLM 출력: \n{output2}")


# 6. 응답을 파이썬에서 쓸 수 있는 형태로 변환
## API가 돌려준 것은 JSON "문자열"이므로 dict로 바꿔야 키로 꺼낼 수 있음
result = json.loads(output2)

print(f"감성 분석 결과: {result['감성 분석 결과']}")
print(f"긍정 키워드: {result['판단 근거 키워드']['긍정']}")
print(f"부정 키워드: {result['판단 근거 키워드']['부정']}")
