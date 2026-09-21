"""TIL: 생성형 AI 활용 - 서울시 공공데이터(추정매출-상권) API 수집 및 삼중 검증 (2026-09-21) — 개념 설명은 README.md 참고"""

import os
import time
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SEOUL_DATA_API_KEY")

if not API_KEY:
    raise ValueError("오류: .env 파일에서 'SEOUL_DATA_API_KEY'를 읽어올 수 없습니다.")

BASE_URL = "http://openapi.seoul.go.kr:8088"
SERVICE_NAME = "VwsmTrdarSelngQq"
PAGE_SIZE = 1000

TARGET_QUARTERS = ["20241", "20242", "20243", "20244", "20251", "20252", "20253", "20254", "20261", "20262"]


def fetch_quarter_data(quarter):
    """특정 분기의 전체 데이터를 1,000건씩 분할 수집하는 함수"""
    start_idx = 1
    end_idx = PAGE_SIZE

    first_url = f"{BASE_URL}/{API_KEY}/json/{SERVICE_NAME}/{start_idx}/{end_idx}/{quarter}"

    try:
        res = requests.get(first_url, timeout=15)
        res.raise_for_status()
        data = res.json()
    except Exception as e:
        print(f"[{quarter}] API 연결 실패: {e}")
        return None, 0

    if SERVICE_NAME not in data:
        result = data.get("RESULT", {})
        code = result.get("CODE", "UNKNOWN")
        msg = result.get("MESSAGE", "API 응답 형식이 올바르지 않습니다.")
        print(f"[{quarter}] API 호출 오류 [{code}]: {msg}")
        return None, 0

    svc_data = data[SERVICE_NAME]
    result_code = svc_data.get("RESULT", {}).get("CODE", "")

    if result_code == "INFO-200":
        print(f"[{quarter}] 데이터 미개설/없음 상태입니다. (응답 코드: {result_code})")
        return None, 0
    elif result_code != "INFO-000":
        msg = svc_data.get("RESULT", {}).get("MESSAGE", "")
        print(f"[{quarter}] API 처리 오류 [{result_code}]: {msg}")
        return None, 0

    total_count = svc_data.get("list_total_count", 0)
    print(f"[{quarter}] API 기준 총 데이터 건수: {total_count:,}건")

    rows = []
    rows.extend(svc_data.get("row", []))

    if total_count > PAGE_SIZE:
        for current_start in range(PAGE_SIZE + 1, total_count + 1, PAGE_SIZE):
            current_end = min(current_start + PAGE_SIZE - 1, total_count)
            url = f"{BASE_URL}/{API_KEY}/json/{SERVICE_NAME}/{current_start}/{current_end}/{quarter}"

            for retry in range(3):
                try:
                    r = requests.get(url, timeout=15)
                    r.raise_for_status()
                    page_json = r.json()
                    rows.extend(page_json.get(SERVICE_NAME, {}).get("row", []))
                    break
                except Exception as e:
                    if retry == 2:
                        print(f"  └ [{quarter}] ({current_start}~{current_end}) 수집 최종 실패: {e}")
                    time.sleep(1)

            time.sleep(0.05)

    return rows, total_count


def run_pipeline():
    verification_summary = []
    all_quarter_dfs = []

    print("\n" + "=" * 70)
    print(" 서울시 상권분석서비스(추정매출-상권) 데이터 수집 및 검증 시작")
    print("=" * 70)

    for quarter in TARGET_QUARTERS:
        print(f"\n▶ [{quarter}] 분기 수집 진행 중...")
        rows, api_total_count = fetch_quarter_data(quarter)

        if not rows or api_total_count == 0:
            verification_summary.append({
                "분기": quarter, "API 표기 건수": 0, "수집 건수": 0,
                "CSV 저장 건수": 0, "검증 결과": "데이터 미제공 (N/A)",
            })
            continue

        collected_count = len(rows)
        df = pd.DataFrame(rows)

        csv_filename = f"seoul_commercial_sales_{quarter}.csv"
        df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

        saved_df = pd.read_csv(csv_filename, encoding="utf-8-sig")
        saved_count = len(saved_df)

        # 삼중 검증 (API 표기 건수 == 메모리 수집 건수 == CSV 저장 행 수)
        is_valid = api_total_count == collected_count == saved_count
        status = "PASS (일치)" if is_valid else "FAIL (불일치)"

        print(f"  ├ API 제공 총 건수 : {api_total_count:,} 건")
        print(f"  ├ 파이썬 수집 건수 : {collected_count:,} 건")
        print(f"  ├ CSV 저장 완료 건수 : {saved_count:,} 건")
        print(f"  └ 수집/저장 검증   : {status}")

        verification_summary.append({
            "분기": quarter, "API 표기 건수": api_total_count,
            "수집 건수": collected_count, "CSV 저장 건수": saved_count, "검증 결과": status,
        })

        all_quarter_dfs.append(df)

    if all_quarter_dfs:
        master_df = pd.concat(all_quarter_dfs, ignore_index=True)
        master_filename = "seoul_commercial_sales_2024Q1_2026Q2_all.csv"
        master_df.to_csv(master_filename, index=False, encoding="utf-8-sig")
        print(f"\n[통합 CSV 저장 완료] {master_filename} (총 {len(master_df):,}건)")

    print("\n" + "=" * 70)
    print("                [ 데이터 수집 및 저장 검증 요약 보고서 ]")
    print("=" * 70)
    report_df = pd.DataFrame(verification_summary)
    print(report_df.to_string(index=False))
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()