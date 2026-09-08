"""TIL: 딕셔너리 전용 함수 - keys/values/items/get (2026-09-08) — 개념 설명은 README.md 참고"""

# 기능: key만 가져오기 -> 변수.keys()
dict_data = {"name": "박보검", "age": 31, "phone": "010-1234-1234"}

keys_data = dict_data.keys()
print(f"전체 key: {keys_data}")

print("-" * 80)

type_info = type(keys_data)
print(f"keys_data의 자료형: {type_info}")

print("-" * 80)

number_keys = len(keys_data)
print(f"추출된 key의 개수: {number_keys}")

# dict_keys 자료형 -> 순서대로 보관하지만 인덱싱은 불가능
# first_element = keys_data[0]  # TypeError 발생

# 기능: value만 가져오기 -> 변수.values()
values_data = dict_data.values()
print(f"전체 values: {values_data}")

print("-" * 80)

number_values = len(values_data)
print(f"추출된 values의 개수: {number_values}")

# 기능: key, value 전체를 가져오기 -> 변수.items()
items_data = dict_data.items()
print(f"전체 key, value 확인: {items_data}")

# 기능: key로 value 가져오기 -> 변수.get("key")
# 방법1: 값 = 변수["key"]
name_info = dict_data["name"]
print(f"name의 값: {name_info}")

print("-" * 80)

# 방법2: 값 = 변수.get("key")
name_info = dict_data.get("name")
print(f"name의 값: {name_info}")

print("-" * 80)

# 존재하지 않는 key 조회 비교
# 방법1: 변수["key"] -> KeyError 발생
# birth_info = dict_data["birth"]

# 방법2: 변수.get("key") -> 에러 없이 None 반환
birth_info = dict_data.get("birth")
print(f"존재하지 않는 key의 값: {birth_info}")