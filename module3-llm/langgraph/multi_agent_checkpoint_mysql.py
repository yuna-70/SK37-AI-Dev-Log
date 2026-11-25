"""TIL: 체크포인터를 SQLite에서 MySQL로 바꾸기 (2026-11-25) — 개념 설명은 README.md 참고"""

## 체인·상태·노드 함수·그래프 구성은 multi_agent_checkpoint_sqlite.py와 완전히 동일함
## 이 파일은 달라지는 부분(체크포인터 연결)만 정리한 것임

import os
import asyncio
from urllib.parse import quote_plus
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.mysql.aio import AIOMySQLSaver


# 1. 환경 설정
file_path = ".env"
output = load_dotenv(file_path, override=True)

print(output)


# 2. aiomysql 호환성 처리
## 설치된 aiomysql 버전에 escape_bytes_prefixed 함수가 없는 경우가 있어
## pymysql 쪽 함수를 가져다 붙이고, 그마저 없으면 직접 만들어 넣음
import aiomysql.connection as _aiomysql_conn
from pymysql import converters as _pymysql_conv

if not callable(_aiomysql_conn.escape_bytes_prefixed):
    if callable(getattr(_pymysql_conv, "escape_bytes_prefixed", None)):
        _aiomysql_conn.escape_bytes_prefixed = _pymysql_conv.escape_bytes_prefixed
    else:
        _aiomysql_conn.escape_bytes_prefixed = lambda val, mapping=None: f"X'{bytes(val).hex()}'"


# 3. MySQL 접속 정보 및 DB URL 구성
## 접속 정보는 .env에서 읽어옴 -> 비밀번호가 코드에 남지 않게 함
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_host = os.getenv("MYSQL_HOST")
mysql_port = os.getenv("MYSQL_PORT")
mysql_db = os.getenv("MYSQL_DB")

## quote_plus(): 비밀번호에 @나 : 같은 기호가 있으면 URL이 엉뚱하게 잘리므로 변환해줌
DB_URL = f"mysql://{mysql_user}:{quote_plus(mysql_password)}@{mysql_host}:{mysql_port}/{mysql_db}"

## URL에 비밀번호가 들어 있으므로 통째로 출력하지 않음
print(f"접속 대상: {mysql_host}:{mysql_port}/{mysql_db}")


# 4. 챗봇 실행
## graph는 multi_agent_checkpoint_sqlite.py에서 만든 것과 동일하다고 가정
async def main(graph):
    ## async with로 비동기 체크포인터 생성
    async with AIOMySQLSaver.from_conn_string(DB_URL) as memory:
        ## 최초 실행 시 체크포인트 저장용 테이블을 자동으로 만들어줌
        ## SQLite 쪽과 달리 setup()을 직접 불러야 함
        ## 이미 테이블이 있으면 "Table 'checkpoint_migrations' already exists" 경고가 뜨지만 정상 동작함
        await memory.setup()

        ## 그래프와 체크포인터 연결
        multi_agent = graph.compile(checkpointer=memory)

        ## 특정 사용자를 구별하기 위한 thread_id 고정
        config = {"configurable": {"thread_id": "user-8888"}}

        print("[비동기 방식 MySQL 기반 멀티 에이전트] 가동 중... (종료: exit)")
        print("=" * 80)

        while True:
            try:
                user_input = input("사용자: ")

                ## 종료 조건
                if user_input.lower() == "exit":
                    print("챗봇을 안전하게 종료합니다.")
                    break

                ## 이번 턴의 질문만 넣음 -> 이전 대화는 체크포인터가 붙여줌
                initial_state = {"messages": [HumanMessage(content=user_input)]}

                final_state = await multi_agent.ainvoke(initial_state, config=config)

                ai_answer = final_state["messages"][-1].content

                print(f"AI 에이전트:\n{ai_answer}")
                print("-" * 80)

            except Exception as e:
                print(f"오류가 발생했습니다.: {e}")
