"""TIL: NumPy 기초 (2026-09-29) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import numpy as np

# 넘파이 배열과 파이썬 리스트 비교

## 파이썬 리스트 데이터 생성
list_data = [1, 2, 3]
print(f"파이썬 리스트: {list_data}")

print("-" * 80)

## 넘파이 배열 생성
arr_data = np.array(list_data)
print(f"넘파이 배열로 변환 후 데이터: {arr_data}")

# python list와 numpy array 차이점 확인

## python list 생성
list_data1 = [1, 2, 3]
list_data2 = [4, 5, 6]

## list 자료형 -> 덧셈 연산 -> 덧셈(X), 리스트의 연결(extension)
output1 = list_data1 + list_data2
print(f"파이썬 리스트에 대한 덧셈 연산의 결과: {output1}")

print("-" * 80)

## numpy array 생성 -> 덧셈 연산
arr_data1 = np.array(list_data1)
arr_data2 = np.array(list_data2)

output2 = arr_data1 + arr_data2
print(f"넘파이 배열에 대한 덧셈 연산의 결과: {output2}")

print("-" * 80)

## 곱셈 연산

### python list 자료형(1): 곱셈 -> 덧셈 반복의 효과
output3 = list_data1 * 3
print(f"파이썬 리스트에 대한 곱셈 연산의 결과: {output3}")

print("-" * 80)

### python list 자료형(2): 곱셈의 결과 실현
output4 = []
for num in list_data1:
    result = num * 3
    output4.append(result)

print(f"파이썬 리스트에 대한 곱셈 연산의 결과: {output4}")

print("-" * 80)

### numpy array 자료형
output5 = arr_data1 * 3
print(f"넘파이 배열에 대한 곱셈 연산의 결과: {output5}")

print("-" * 80)

## 통계 처리(평균값 구하기)

### python list 자료형
list_avg = sum(list_data1) / len(list_data1)
print(f"파이썬 리스트에 대한 평균값: {list_avg}")

print("-" * 80)

### numpy array 자료형
arr_avg = arr_data1.mean()
print(f"넘파이 배열에 대한 평균값: {arr_avg}")

# 대괄호가 중첩된 구조의 리스트 생성

## 대괄호가 중첩된 파이썬 리스트 자료형 생성(반드시 성분 원소 리스트의 원소의 개수가 동일)
list_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(f"리스트를 성분 원소로 하는 리스트: {list_data}")

print("-" * 80)

## 넘파이 배열로 변환
arr_data = np.array(list_data)
print(f"리스트를 성분 원소로 하는 리스트를 넘파이 배열로 변환한 결과: \n{arr_data}")

# 파이썬 리스트 자료형에 대한 인덱싱

## 리스트 자료형 데이터 생성
list_data = [[1, 2, 3], [4, 5, 6]]
print(f"생성된 리스트 데이터: \n{list_data}")

print("-" * 80)

## 1단계: 전체 리스트 -> 0번 원소 인덱싱
output1 = list_data[0]
print(f"전체 리스트에서 0번 원소를 인덱싱한 결과: \n{output1}")

print("-" * 80)

## 2단계: 첫 번째 성분 원소(리스트) -> 0번 원소 인덱싱
output2 = output1[0]
print(f"첫 번째 성분 원소에서 0번 원소 인덱싱: {output2}")

print("-" * 80)

## 정리: 숫자 1 추출 -> 인덱싱 -> 변수[인덱스][인덱스]
output3 = list_data[0][0]
print(f"숫자 1을 인덱싱한 결과: {output3}")

# 넘파이 배열 자료형에 대한 인덱싱

## list_data -> 넘파이 배열 생성
arr_data = np.array(list_data)
print(f"2차원 배열: \n{arr_data}")

print("-" * 80)

## 숫자 1 추출 -> 인덱싱 -> 파이썬 리스트에 대한 인덱싱처럼 적용
output1 = arr_data[0][0]
print(f"숫자 1을 인덱싱한 결과: {output1}")

print("-" * 80)

## 숫자 1 추출 -> 인덱싱 -> 구조(행, 열)을 이용한 인덱싱
output2 = arr_data[0, 0]
print(f"숫자 1을 인덱싱한 결과: {output2}")

# 2차원 배열 슬라이싱

## range 함수 사용 -> 0~39 사이의 연속적인 정수 데이터 생성
list_data = [range(0, 10), range(10, 20), range(20, 30), range(30, 40)]

## 넘파이 배열 생성
arr_data = np.array(list_data)
print(f"생성된 2차원 배열: \n{arr_data}")

print("-" * 80)

## 행 인덱스 전체, 열 인덱스 4부터 8까지 슬라이싱
arr_data1 = arr_data[:, 4:9]
print(f"슬라이싱 결과: \n{arr_data1}")