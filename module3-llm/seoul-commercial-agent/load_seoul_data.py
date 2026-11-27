"""TIL: 서울시 상권 매출 CSV를 MySQL에 적재하기 (2026-11-27) — 개념 설명은 README.md 참고"""

import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


# 1. 환경 설정
load_dotenv(".env", override=True)


# 2. 한글 컬럼명을 영문으로 바꾸기 위한 매핑 딕셔너리
## MySQL 컬럼명에 한글을 쓰면 SQL을 쓸 때마다 백틱으로 감싸야 하고,
## 나중에 LLM에게 SQL을 생성시킬 때도 영문 쪽이 훨씬 안정적임
## 공공데이터 원본의 영문 코드명을 그대로 사용
column_mapping = {
    "기준_년분기_코드": "STDR_YYQU_CD",
    "상권_구분_코드": "TRDAR_SE_CD",
    "상권_구분_코드_명": "TRDAR_SE_CD_NM",
    "상권_코드": "TRDAR_CD",
    "상권_코드_명": "TRDAR_CD_NM",
    "서비스_업종_코드": "SVC_INDUTY_CD",
    "서비스_업종_코드_명": "SVC_INDUTY_CD_NM",
    "당월_매출_금액": "THSMON_SELNG_AMT",
    "당월_매출_건수": "THSMON_SELNG_CO",
    "주중_매출_금액": "MDWK_SELNG_AMT",
    "주말_매출_금액": "WKEND_SELNG_AMT",
    "월요일_매출_금액": "MON_SELNG_AMT",
    "화요일_매출_금액": "TUES_SELNG_AMT",
    "수요일_매출_금액": "WED_SELNG_AMT",
    "목요일_매출_금액": "THUR_SELNG_AMT",
    "금요일_매출_금액": "FRI_SELNG_AMT",
    "토요일_매출_금액": "SAT_SELNG_AMT",
    "일요일_매출_금액": "SUN_SELNG_AMT",
    "시간대_00~06_매출_금액": "TMZON_00_06_SELNG_AMT",
    "시간대_06~11_매출_금액": "TMZON_06_11_SELNG_AMT",
    "시간대_11~14_매출_금액": "TMZON_11_14_SELNG_AMT",
    "시간대_14~17_매출_금액": "TMZON_14_17_SELNG_AMT",
    "시간대_17~21_매출_금액": "TMZON_17_21_SELNG_AMT",
    "시간대_21~24_매출_금액": "TMZON_21_24_SELNG_AMT",
    "남성_매출_금액": "ML_SELNG_AMT",
    "여성_매출_금액": "FML_SELNG_AMT",
    "연령대_10_매출_금액": "AGRDE_10_SELNG_AMT",
    "연령대_20_매출_금액": "AGRDE_20_SELNG_AMT",
    "연령대_30_매출_금액": "AGRDE_30_SELNG_AMT",
    "연령대_40_매출_금액": "AGRDE_40_SELNG_AMT",
    "연령대_50_매출_금액": "AGRDE_50_SELNG_AMT",
    "연령대_60_이상_매출_금액": "AGRDE_60_ABOVE_SELNG_AMT",
    "주중_매출_건수": "MDWK_SELNG_CO",
    "주말_매출_건수": "WKEND_SELNG_CO",
    "월요일_매출_건수": "MON_SELNG_CO",
    "화요일_매출_건수": "TUES_SELNG_CO",
    "수요일_매출_건수": "WED_SELNG_CO",
    "목요일_매출_건수": "THUR_SELNG_CO",
    "금요일_매출_건수": "FRI_SELNG_CO",
    "토요일_매출_건수": "SAT_SELNG_CO",
    "일요일_매출_건수": "SUN_SELNG_CO",
    ## 원본 CSV의 건수 컬럼명이 "시간대_건수~06_매출_건수"처럼 되어 있어 그대로 적음
    "시간대_건수~06_매출_건수": "TMZON_00_06_SELNG_CO",
    "시간대_건수~11_매출_건수": "TMZON_06_11_SELNG_CO",
    "시간대_건수~14_매출_건수": "TMZON_11_14_SELNG_CO",
    "시간대_건수~17_매출_건수": "TMZON_14_17_SELNG_CO",
    "시간대_건수~21_매출_건수": "TMZON_17_21_SELNG_CO",
    "시간대_건수~24_매출_건수": "TMZON_21_24_SELNG_CO",
    "남성_매출_건수": "ML_SELNG_CO",
    "여성_매출_건수": "FML_SELNG_CO",
    "연령대_10_매출_건수": "AGRDE_10_SELNG_CO",
    "연령대_20_매출_건수": "AGRDE_20_SELNG_CO",
    "연령대_30_매출_건수": "AGRDE_30_SELNG_CO",
    "연령대_40_매출_건수": "AGRDE_40_SELNG_CO",
    "연령대_50_매출_건수": "AGRDE_50_SELNG_CO",
    "연령대_60_이상_매출_건수": "AGRDE_60_ABOVE_SELNG_CO",
}


# 3. CSV 파일을 DataFrame으로 변환
## 공공데이터포털에서 받은 파일은 보통 cp949로 저장되어 있음
## utf-8로 읽으면 UnicodeDecodeError가 남
file_path = "seoul_data.csv"

df = pd.read_csv(file_path, encoding="cp949")

print(f"[CSV 로드 완료] 행: {len(df)}개, 컬럼: {list(df.columns)}")
print(df.head())


# 4. 컬럼명 정리
## 4-1. 양끝 공백 제거
## df.columns는 Index 자료형이라 .str을 거쳐야 문자열 전용 함수를 쓸 수 있음
df.columns = df.columns.str.strip()

## 4-2. 영문 컬럼명으로 일괄 변경
df1 = df.rename(columns=column_mapping)

print(df1.head())


# 5. 매핑 누락 컬럼 검증
## 바꾼 뒤 눈으로 확인하지 않고, 남은 한글 컬럼이 있는지 코드로 확인함
expected_cols = list(column_mapping.values())

unmapped_cols = []

for col in df1.columns:
    if col not in expected_cols:
        unmapped_cols.append(col)

## 빈 리스트는 False로 판정됨
if unmapped_cols:
    print(f"매핑되지 않은 컬럼이 있습니다. 해당 컬럼 목록을 확인하세요: {unmapped_cols}")
else:
    print("모든 컬럼이 성공적으로 매핑되었습니다.")


# 6. MySQL 접속 URL 생성
## URL.create()를 쓰면 비밀번호에 특수문자가 있어도 알아서 처리해줌
## 접속 정보는 .env에서 읽어와 코드에 비밀번호가 남지 않게 함
db_url = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    database=os.getenv("MYSQL_DB"),
    ## 한글을 포함한 문자열을 제대로 저장하려면 utf8mb4가 필요함
    query={"charset": "utf8mb4"},
)

## URL.create()로 만든 객체는 print할 때 비밀번호를 ***로 가려줌
print(f"db_url: {db_url}")


# 7. DB 연결
table_name = "seoul_commercial"
engine = create_engine(db_url)

print("DB 연결 성공")


# 8. DataFrame을 MySQL 테이블에 저장 및 검증
try:
    ## if_exists 옵션
    ##   "replace": 기존 테이블 덮어쓰기
    ##   "append": 기존 데이터에 추가
    ##   "fail": 테이블이 있으면 오류
    df1.to_sql(
        name=table_name,
        con=engine,
        ### 반복 실행 시 중복 방지를 위해 replace 사용
        if_exists="replace",
        ### DataFrame의 인덱스를 별도 컬럼으로 저장하지 않음
        index=False,
        ### 12만 행을 한 번에 보내면 메모리와 패킷 크기 문제가 생기므로 1,000행씩 나눠 보냄
        chunksize=1000,
    )

    print(f"{table_name} 테이블에 {len(df)}건 저장 성공!")
    print("-" * 80)

    ## 저장된 데이터를 다시 조회해 건수가 맞는지 확인
    query = f"SELECT * FROM {table_name}"
    df_result = pd.read_sql(sql=query, con=engine)

    print(f"[MySQL 조회 결과] 총 {len(df_result)}건")
    print(df_result.head())

except Exception as e:
    print(f"DB 작업 중 오류 발생: {e}")
