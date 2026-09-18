"""TIL: 생성형 AI 활용 - 인기 도서 200권 수집 및 CSV 저장 (2026-09-18) — 개념 설명은 README.md 참고"""

import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def fetch_popular_books():
    # 1. 설정 정보 지정
    AUTH_KEY = os.getenv("LIBRARY_AUTH_KEY")
    BASE_URL = "http://data4library.kr/api/loanItemSrch"

    params = {
        "authKey": AUTH_KEY,
        "startDt": "2025-01-01",
        "endDt": "2026-06-30",
        "age": "20",
        "pageNo": "1",
        "pageSize": "200",
        "format": "json",
    }

    print("API 호출을 시작합니다...")

    # 2. API 호출 및 데이터 수신
    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[오류] API 네트워크 요청 실패: {e}")
        return
    except ValueError:
        print("[오류] 응답 데이터를 JSON 형식으로 파싱할 수 없습니다.")
        return

    # 3. 응답 데이터 파싱 및 가공
    try:
        response_data = data.get("response", {})

        if "error" in response_data:
            print(f"[API 오류] {response_data['error']}")
            return

        docs = response_data.get("docs", [])

        if not docs:
            print("[경고] 수집된 도서 데이터가 없습니다. 파라미터나 인증키를 확인해주세요.")
            return

        book_list = []
        for item in docs:
            doc = item.get("doc", {})
            book_info = {
                "순위": doc.get("ranking"),
                "순번": doc.get("no"),
                "도서명": doc.get("bookname"),
                "저자명": doc.get("authors"),
                "출판사": doc.get("publisher"),
                "출판년도": doc.get("publication_year"),
                "13자리 ISBN": doc.get("isbn13"),
                "ISBN 부가기호": doc.get("addition_symbol"),
                "권": doc.get("vol"),
                "주제분류코드": doc.get("class_no"),
                "주제분류명": doc.get("class_nm"),
                "대출건수": doc.get("loan_count"),
                "책표지 URL": doc.get("bookImageURL"),
                "도서 상세 페이지 URL": doc.get("bookDtlUrl"),
            }
            book_list.append(book_info)

        # 4. Pandas DataFrame 변환 및 CSV 저장
        df = pd.DataFrame(book_list)
        output_filename = "popular_books_20s_2025_2026.csv"
        df.to_csv(output_filename, index=False, encoding="utf-8-sig")

        print("=" * 60)
        print(" 성공적으로 데이터 수집이 완료되었습니다!")
        print(f" 총 수집 건수: {len(df)}건")
        print(f" 저장 파일명: {os.path.abspath(output_filename)}")
        print("=" * 60)

        print("\n[수집 데이터 미리보기 (상위 5건)]")
        print(df[["순위", "도서명", "저자명", "출판사", "대출건수"]].head())

    except KeyError as e:
        print(f"[오류] 데이터 파싱 중 키 구조를 찾을 수 없습니다: {e}")
    except Exception as e:
        print(f"[오류] 알 수 없는 에러 발생: {e}")


if __name__ == "__main__":
    fetch_popular_books()