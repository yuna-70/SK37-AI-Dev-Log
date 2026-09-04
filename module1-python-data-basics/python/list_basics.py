# 리스트 생성

# 데이터가 없는 리스트 자료형 생성
list = []
print(list)

# 숫자 리스트 자료형 생성
list_data1 = [0, 1, 2, 3, 4, 5]
print(list_data1)

# 문자열 리스트 자료형 생성
list_data2 = ["My", "name", "is", "YN"]
print(list_data2)

# 숫자, 문자열 혼합 리스트 자료형 생성
list_data3 = [1, 2, ["My", "name"]]
print(list_data3)

# 인덱싱
list_data = [10, 20, 30, 40, 50]

# 첫 번째 인덱스
first_idx = list_data[0]
print(f"첫 번째 인덱스 : {first_idx}")
# print(f'첫 번째 인덱스 : {list_data[0]}')
# ---first_idx-print 문을 사용하는 이유 ---
# 변수명을 통해 쉽게 이해할 수 있음
# 값에 의미를 부여할 땐 변수로 빼두는 습관이 좋음
# list_data[0]을 코드 여러 군데서 사용하면 모두 고쳐야 함

# 마지막 인덱스
last_idx = list_data[-1]
print(f"마지막 인덱스 : {last_idx}")

# 인덱싱 실습
# list_data1에서 문자 ‘b’만 뽑아서 출력하기
list_data1 = [1, 2, 3, ['a', 'b', 'c']]
print(list_data1)

find_idx = list_data1[3][1]
print(find_idx)

# 'b'를 찾는 과정

## 첫 번째 인덱싱
first_element = list_data1[0]
print(f'첫 번째 : {first_element}')

## 두 번째 인덱싱
second_element = list_data1[1]
print(f'두 번째 : {second_element}')

## 세 번째 인덱싱
third_element = list_data1[2]
print(f'세 번째 : {third_element}')

## 네 번째 인덱싱
fourth_element = list_data1[3]
list_data2 = list_data1[3]
print(f'네 번째 : {list_data2}')

## 네 번째 -> 리스트 자료형 -> 인덱싱 -> 변수[인덱스]
# output = list_data2[1]
output = list_data1[3][1]
print(f'네 번째 데이터의 두 번째 : {output}')

# 슬라이싱
list_data = [0, 10, 20, 30, 40]

# 첫 번째부터 세 번째까지 슬라이싱
list_data1 = list_data[0:3]
print(f"첫 번째부터 세 번째까지 슬라이싱 : {list_data1}")

# 네 번째부터 마지막까지 슬라이싱 
list_data2 = list_data[3:]
print(f"네 번째부터 마지막까지 슬라잇이 : {list_data2}")


