"""TIL: NumPy · pandas 복습 문제 10문제 (2026-09-30) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import numpy as np
import pandas as pd

# [넘파이] 문제 1
# 배열 생성 및 덧셈 연산
# 파이썬 리스트 [10, 20, 30]과 [1, 2, 3]을 각각 넘파이 배열로 생성하고,
# 두 배열을 더한 결과를 출력하는 코드를 작성하세요.
list1 = [10, 20, 30]
list2 = [1, 2, 3]

arr_data1 = np.array(list1)
arr_data2 = np.array(list2)

sum_result = arr_data1 + arr_data2
print(f"덧셈 결과: {sum_result}")

# [넘파이] 문제 2
# 곱셈 연산
# 리스트 data = [5, 10, 15]의 모든 원소에 3을 곱한 결과를 얻고자 합니다.
# 넘파이 배열의 연산 특성을 이용하여 반복문 없이 결과를 출력하는 코드를 작성하세요.
list_data = [5, 10, 15]
arr_data = np.array(list_data)

multi_result = arr_data * 3
print(f"배열 곱셈 결과: {multi_result}")

# [넘파이] 문제 3
# 평균값 구하기
# 넘파이 배열 arr = np.array([10, 30, 50, 70, 90])의 평균값을
# 넘파이 전용 메서드를 사용하여 계산하고 출력하세요.
arr = np.array([10, 30, 50, 70, 90])

# 메서드(객체.기능()) 방식 -> arr.mean()
average = arr.mean()
print(f"평균값: {average}")

# [넘파이] 문제 4
# 2차원 배열 생성
# 리스트 [[10, 20], [30, 40]]를 넘파이 배열로 변환하여
# 2행 2열의 구조를 가진 배열을 생성하고 출력하세요.
list_2d = [[10, 20], [30, 40]]
arr_2d = np.array(list_2d)

print(f"2차원 배열: \n{arr_2d}")

# [넘파이] 문제 5
# 2차원 배열 인덱싱
# 문제 4에서 생성한 배열에서 숫자 40을 추출하고자 합니다.
# 넘파이의 구조(행, 열)를 이용한 인덱싱 방식(arr[행, 열])으로 코드를 작성하세요.

# 40은 1행 1열에 위치함 (인덱스는 0부터 시작)
result = arr_2d[1, 1]
print(f"추출된 숫자: {result}")

# [pandas] 문제 1
# 데이터 불러오기
# pd.read_csv()를 사용하여 ad_performance.csv 파일을 불러와 변수 df에 저장하고,
# display 함수를 이용하여 전체 데이터를 확인하는 코드를 작성하세요.
file_path = "ad_performance.csv"
df = pd.read_csv(file_path)

display(df)

# [pandas] 문제 2
# 인덱스 확인
# 불러온 데이터프레임(df)에서 전체 컬럼명(Columns) 정보만 추출하여 출력하세요.
info_columns = df.columns
print(f"컬럼 인덱스: \n{info_columns}")

# [pandas] 문제 3
# 특정 컬럼 선택 (Fancy Indexing)
# df에서 "Channel", "Age_Group", "Revenue" 세 개의 컬럼만 선택하여
# 새로운 데이터프레임 df_sub를 생성하세요.
df_sub = df[["Channel", "Age_Group", "Revenue"]]
print(f"선택한 컬럼: \n{df_sub}")

# [pandas] 문제 4
# 새로운 컬럼 추가
# 클릭당 비용을 의미하는 "CPC" 컬럼을 추가하세요. (공식: Cost / Clicks)
df["CPC"] = df["Cost"] / df["Clicks"]

display(df)

# [pandas] 문제 5
# 빈도수 계산
# "Age_Group" 컬럼에 있는 각 항목별(20s, 30s 등) 데이터의 빈도수를 확인하세요.
df_age = df["Age_Group"].value_counts()
print(f"연령대별 빈도수: \n{df_age}")