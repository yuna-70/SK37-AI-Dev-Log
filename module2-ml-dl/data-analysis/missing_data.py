"""TIL: 누락 데이터 처리 (2026-09-30) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기

## 파일 경로 설정
file_path = "ns_202104.csv"

## DataFrame 생성
df_ns = pd.read_csv(file_path)

## 결과 확인
display(df_ns)

# 각 컬럼별 누락 데이터의 수 확인

## 1단계: isnull() 함수 적용 -> 불리언 데이터로 표현되는 DataFrame 생성
df_bool = df_ns.isnull()
display(df_bool)

print("-" * 80)

## 2단계: sum() 함수 적용 -> 각 컬럼별 누락 데이터 개수 연산
## df_bool.sum()과 동일하며, 두 단계를 한 줄로 연결해서 사용
number_nulls = df_ns.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{number_nulls}")

# 누락된 데이터 삭제

## 목표: 누락 데이터가 존재하는 모든 행 삭제 -> df.dropna(ignore_index=True)
## 401,682행 -> 35,827행 (91% 삭제)
df_ns1 = df_ns.dropna(ignore_index=True)
display(df_ns1)

## 목표: 특정 컬럼의 누락만 제거 -> df.dropna(subset=[col1, col2, ...], ignore_index=True)
## 특정 컬럼: "도서명", "저자" -> 401,081행 유지
df_ns2 = df_ns.dropna(subset=["도서명", "저자"], ignore_index=True)
display(df_ns2)

# 누락 데이터 대체

## 목표: "없음" 문자열로 대체 -> df.fillna(값)
df_ns3 = df_ns.fillna("없음")
display(df_ns3)