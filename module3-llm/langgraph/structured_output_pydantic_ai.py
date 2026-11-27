"""TIL: PydanticAI Agent로 LLM 출력 구조화하기 (2026-11-27) — 개념 설명은 README.md 참고"""

import json
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from langgraph.graph import StateGraph, END


# 1. 환경 설정
file_path = ".env"
output = load_dotenv(file_path)

print(output)


# 2. 그래프 상태 정의
class AgentState(BaseModel):
    ## 사용자의 요청 사항 저장
    request: str = ""
    ## LLM이 출력한 원시 텍스트
    raw_response: str = ""
    ## 구조화된 결과 데이터
    structured_data: dict = {}
    ## 에러 발생 시 기록할 메시지
    error_message: str = ""


# 3. [제1부] 실패 시나리오
## 비구조화된 텍스트가 다음 노드를 어떻게 망가뜨리는지 보여주는 예시


## 3-1. 분석 노드
## 실제 LLM 대신, 형식을 안 지킨 응답을 흉내만 냄
async def unsafe_research_node(state: AgentState):
    print("[Node 1] 제조 현장 자재 수량 데이터 분석 중...")

    ## 안내문 + 코드블록 + 안내문이 섞여 있고, 따옴표도 JSON 규격이 아님
    ## current_stock에는 숫자가 아니라 문장이 들어 있음
    llm_bad_output = """
    네, 요청하신 자재 재고 분석 결과입니다!
    ```json
    {
    'item_name': '고강도 볼트M8',
    'current_stock': '수량 부족 (재고 15개)'
    }
    ```
    추가 조치가 필요하면 말씀하세요.
    """

    return {"raw_response": llm_bad_output}


## 3-2. 가공 처리 노드
## 넘겨받은 텍스트에서 JSON을 직접 잘라내 정수 연산을 시도함
async def unsafe_process_node(state: AgentState) -> dict:
    print("[Node 2] 분석된 데이터를 바탕으로 자동 발주 수량 계산 시작...")
    print("-" * 80)

    print(f"state: \n{state}")
    print("-" * 80)

    ## 앞 노드가 남긴 비구조화된 원시 텍스트
    raw_text = state.raw_response

    try:
        ### 코드블록 사이만 잘라내기
        ### 주의: 원문의 구분자는 백틱 세 개(```)인데 작은따옴표 세 개를 찾고 있음
        ### 그래서 split 결과가 1개짜리 리스트가 되어 [1]에서 먼저 멈춤
        bad_json_str = raw_text.split("'''json")[1].split("'''")[0].strip()

        ### 작은따옴표를 큰따옴표로 바꿔야 JSON으로 읽힘
        clean_json_str = bad_json_str.replace("'", '"')

        data = json.loads(clean_json_str)

        ### 숫자가 와야 할 자리에 "수량 부족 (재고 15개)"라는 문장이 들어 있음
        stock_count = data["current_stock"]
        print(f"현재 재고가 {stock_count}개 확인되었습니다.")
        print("-" * 80)

        ### 안전 수량 기준으로 부족분 계산 -> 문자열이면 여기서 터짐
        default_qty = 100
        order_qty = default_qty - stock_count

        return {"structured_data": {"item": data["item_name"], "order_qty": order_qty}}

    except Exception as e:
        error_msg = f"에러 발생! 에러 내용: {e}"
        return {"error_message": error_msg}


## 3-3. 그래프 생성 및 컴파일
unsafe_workflow = StateGraph(AgentState)

unsafe_workflow.add_node("research", unsafe_research_node)
unsafe_workflow.add_node("process", unsafe_process_node)

unsafe_workflow.set_entry_point("research")

unsafe_workflow.add_edge("research", "process")
unsafe_workflow.add_edge("process", END)

unsafe_agent = unsafe_workflow.compile()


## 3-4. 실행 및 결과 확인
async def run_unsafe():
    initial_state = {
        "request": "현재 참고 확인 결과 고강도 볼트 M8의 수량이 부족하여 경고 알림(실재고는 현재 15개 남음). 조속히 처리 요망"
    }

    unsafe_state = await unsafe_agent.ainvoke(initial_state)

    if unsafe_state.get("error_message"):
        print(f"\n[결과 알림] {unsafe_state['error_message']}")
        print("한 노드의 비구조화된 출력이 에이전트 전체 파이프라인을 중단시켰습니다.")


# 4. [제2부] PydanticAI로 구조화된 출력 (성공 시나리오)


## 4-1. LLM이 지켜야 할 출력 형식 정의
## 상태를 정의할 때와 똑같이 BaseModel을 상속함
## description은 LLM에게 주는 안내문이고, 실제로 검사하는 것은 "타입"임
## current_stock을 str로 두면 "15"가 들어와 뒤에서 100 - "15"로 터짐
class InventoryAnalysis(BaseModel):
    item_name: str = Field(description="자재 품목 명칭")
    current_stock: int = Field(description="현재 창고에 남아있는 정확한 재고 수량 (숫자만 허용)")


## 4-2. PydanticAI Agent 정의
## ChatOpenAI(model="gpt-5-nano") 자리를 대신함
## output_type에 지정한 형식을 LLM이 지키도록 강제하고, 어기면 다시 시도하게 함
pydantic_agent = Agent(
    model="openai:gpt-5-nano",
    output_type=InventoryAnalysis,
    system_prompt="당신은 제조 공장의 자재 관리 전문가입니다. 텍스트 문맥을 분석하고 재고 수량을 정확한 정수(int)로만 추출하시오.",
)


## 4-3. 안전한 분석 노드
async def safe_research_node(state: AgentState) -> dict:
    print("[Node 1] PydanticAI 기반 자재 데이터 분석 중 ...")
    print("-" * 80)

    user_request = state.request

    print(f"요청 사항: {user_request}")
    print("-" * 80)

    user_prompt = f"다음 요청에서 품목 명칭과 현재 재고 수량을 정수로 추출해줘: {user_request}"

    ## run()은 async 함수라 await를 붙여야 실행됨
    ## await pydantic_agent.run(...).output 처럼 쓰면 .output이 먼저 평가되어
    ## 아직 실행되지 않은 코루틴 객체에서 꺼내려 하므로 AttributeError가 남
    agent_result = await pydantic_agent.run(user_prompt=user_prompt)

    print(f"pydantic_agent 실행 결과: \n{agent_result}")
    print("-" * 80)

    ## AgentRunResult에서 실제 결과물만 꺼냄 -> InventoryAnalysis 객체
    agent_output = agent_result.output

    print(f"pydantic_agent 실행 결과: {agent_output}")
    print("-" * 80)

    ## BaseModel 전용 함수 model_dump()로 딕셔너리 변환
    ## item_name='고강도 볼트 M8' current_stock=15 -> {'item_name': ..., 'current_stock': 15}
    agent_output_dict = agent_output.model_dump()

    return {"structured_data": agent_output_dict}


## 4-4. 가공 처리 노드
## 파싱이 전혀 필요 없음. 딕셔너리에서 바로 꺼내 연산함
async def safe_process_node(state: AgentState) -> dict:
    print("[Node 2] 구조화된 데이터를 바탕으로 부족한 수량 연산 시작 ...")
    print("-" * 80)

    data = state.structured_data

    stock_count = data["current_stock"]

    print(f"현재 재고가 정확히 '{stock_count}'개 확인되었습니다.")
    print("-" * 80)

    default_qty = 100
    order_qty = default_qty - stock_count

    print(f"[자동 발주 확정] 품목: {data['item_name']} | 발주 필요 수량: {order_qty}개")
    print("-" * 80)

    return {"error_message": "없음 (비동기 파이프라인 성공)"}


## 4-5. 그래프 생성 및 컴파일
safe_workflow = StateGraph(AgentState)

safe_workflow.add_node("safe_research", safe_research_node)
safe_workflow.add_node("safe_process", safe_process_node)

safe_workflow.set_entry_point("safe_research")

safe_workflow.add_edge("safe_research", "safe_process")
safe_workflow.add_edge("safe_process", END)

safe_agent = safe_workflow.compile()


## 4-6. 실행 및 결과 확인
async def run_safe():
    initial_state = {
        "request": "현재 참고 확인 결과 고강도 볼트 M8의 수량이 부족하여 경고 알림(실재고는 현재 15개 남음). 조속히 조치 요망"
    }

    print("에이전트 시스템 가동 ...")
    print("-" * 80)

    final_state = await safe_agent.ainvoke(initial_state)

    error_msg = final_state["error_message"]
    print(f"[최종 결과]: {error_msg}")


# 5. 실행
## 주피터 노트북에서는 await run_unsafe() / await run_safe()로 바로 실행
async def main():
    await run_unsafe()
    print("=" * 80)
    await run_safe()


if __name__ == "__main__":
    asyncio.run(main())
