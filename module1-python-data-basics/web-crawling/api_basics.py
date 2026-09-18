"""TIL: Open API 기초 - requests, JSON 파싱, DataFrame, CSV 저장 (2026-09-18) — 개념 설명은 README.md 참고"""

import os
import requests
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
AUTH_KEY = os.getenv("LIBRARY_AUTH_KEY")

# 호출 URL 작성 (도서관 정보나루)
url = f"http://data4library.kr/api/loanItemSrch?authKey={AUTH_KEY}&startDt=2025-01-01&endDt=2026-06-30&age=20&format=json"

# 인기 대출 도서 정보 요청하고 결과값 가져오기
data = requests.get(url).text

# json 문자열 -> python dict 자료형으로 변환
dict_data = json.loads(data)

# "docs" 도서 정보 추출 (중첩 딕셔너리를 단계별로 확인)
first_keys = dict_data.keys()
# dict_keys(['response'])

first_values = dict_data.get("response")

second_keys = first_values.keys()
# dict_keys(['request', 'resultNum', 'numFound', 'docs'])

output = dict_data.get("response").get("docs")

# 도서 정보 저장할 빈 리스트 작성
info_book = []

# 도서 정보 반복하기
for book in output:
    value = book.get("doc")
    info_book.append(value)

# DataFrame 변환 및 CSV 저장
data_table = pd.DataFrame(info_book)
print(data_table)

file_path = "book_info_test.csv"
data_table.to_csv(file_path)