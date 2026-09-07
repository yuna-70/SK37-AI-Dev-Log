"""TIL: Tuple - 리스트와의 공통점/차이점 (2026-09-07) — 개념 설명은 README.md 참고"""

list_data = [1, 2, 3]
print(f"리스트 자료형 : {list_data}")

tuple_data = (1, 2, 3)
print(f"튜플 자료형 : {tuple_data}")

# 공통점: 순서형 묶음 자료형 -> 인덱싱 가능
first_element_list = list_data[0]
print(f"리스트 자료형의 첫 번째 데이터 : {first_element_list}")

first_element_tuple = tuple_data[0]
print(f"튜플 자료형의 첫 번째 데이터 : {first_element_tuple}")

# 차이점: 값 수정 -> 리스트 가능, 튜플 불가능
list_data[0] = "mango"
print(f"데이터 수정 후 리스트 자료형 : {list_data}")

# tuple_data[0] = "mango"  # TypeError 발생 (튜플은 수정 불가)