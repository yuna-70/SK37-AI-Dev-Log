"""TIL: 프롬프트 엔지니어링 - JSON 형식 요청과 출력 형식 지정 (2026-11-12) — 개념 설명은 README.md 참고"""

from dotenv import load_dotenv
from openai import OpenAI


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(f".env 파일 로드 결과: {output}")

client = OpenAI()


# 2. 방법 1: JSON 형식으로 결과물 요청하기
## 2-1. 실행 함수 정의
def get_json_completion(prompt, model="gpt-5-nano"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "너는 사용자의 요청에 충실하고 정확한 답변을 제공하는 AI 비서야"},
            {"role": "user", "content": prompt},
        ],
        ## 응답 형식을 JSON 문자열로 고정
        response_format={"type": "json_object"},
    )
    return response.choices[0].message.content


## 2-2. 사용할 키를 직접 지정 -> 받는 쪽에서 파싱하기 쉬워짐
user_prompt = """
3개의 가상의 책 제목, 저자, 장르를 생성해 줘.
아래 키를 사용하여 JSON 형식으로 제공해야 돼:
book_id, title, author, genre
"""

output = get_json_completion(prompt=user_prompt)

print(f"LLM 응답: \n{output}")


# 3. 방법 2: 출력 형식 지정하기
## 3-1. 실행 함수 정의
## 자유 서술형 답변이므로 response_format을 지정하지 않음
def get_completion(prompt, model="gpt-5-nano"):
    response = client.chat.completions.create(
        model=model,
        ## 역할 부여: 분야를 구체적으로 지정할수록 답변의 전문성이 올라감
        messages=[
            {
                "role": "system",
                "content": '너는 "친환경/지속가능성"과 "웰빙" 분야를 전문으로 하는 최고 수준의 디지털 마케팅 전문가야.',
            },
            {"role": "user", "content": prompt},
        ],
    )
    return response.choices[0].message.content


## 3-2. 구체적 지시 + 맥락 제시 + 예시 활용을 한 프롬프트에 모두 적용
user_prompt = """
< >로 구분된 핵심 목표와 제품 정보를 바탕으로 '생분해성 요가 매트'의 성공적인 시장 안착을 위한 디지털 마케팅 전략을 수립하여 제시하십시오.

<핵심 목표>
3개월 내 월 판매량 200개 달성 및 친환경 요가 매트 시장 내 브랜드 인지도 확립

<제품 정보>
1.제품: 생분해성 요가 매트
2.핵심 가치: 친환경, 지속 가능성, 뛰어난 그립감과 편안함, 유해 물질 무첨가
3.타겟 고객: 환경 보호에 관심이 많고 요가를 즐겨 하는 20대 후반 ~ 40대 중반 여성
4.타겟 고객의 특징: 온라인 정보 탐색에 능숙하며, 가치 소비를 지향하고, 건강과 웰빙에 투자하는 경향이 있음.
5.월별 예산: 300만원 (총 3개월간 900만원)
6.기간: 3개월
7.주요 목표: 3개월 내 월 판매량 200개 달성 및 친환경 요가 매트 시장 내 브랜드 인지도 확립

제시하는 전략은 다음 항목들을 반드시 포함해야 합니다. 각 항목은 매우 구체적이고 즉시 실행 가능한 내용으로 구성되어야
하며, 단순한 나열을 넘어 각 전략의 핵심 의도와 기대 효과를 명확히 설명해 주세요.

1.  전략 개요 및 핵심 메시지:
    * 제품의 친환경적 가치와 타겟 고객의 니즈를 연결하는 핵심 메시지 3가지를 명확히 제시하십시오.
    * 3개월 전략의 전반적인 방향성을 단계별로 요약하십시오 (예: 인지도 확산 → 구매 유도 → 재구매 및 충성도 강화).

2.  타겟 고객 상세 분석:
    * 타겟 고객의 특성, 온라인 활동 패턴, 구매 동기, Pain Points 등을 심층적으로 분석하여 제시하십시오.

출력 형식:
다음 ```형식 지침```과 <예시>를 철저히 준수하여 응답을 작성하십시오.

```형식 지침```
각 섹션은 <예시>와 같이 가독성 높은 리스트(-) 또는 문단으로 구성해 주세요.
불필요한 서문이나 맺음말 없이 요청된 내용만을 작성하십시오.

<예 시>
1. 전략 개요 및 핵심 메시지
- [핵심 메시지 1]
- [핵심 메시지 2]
- 전반적인 전략 방향 요약: [내용]
2. 타겟 고객 상세 분석
- [특성 1]
- [특성 2]
- [온라인 활동 패턴]
- [Pain Points]
- [제품을 통한 해결책]
"""

output = get_completion(prompt=user_prompt)

print(f"LLM 출력: \n{output}")
