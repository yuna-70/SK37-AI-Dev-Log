"""TIL: 리스트 전용 함수 - append/extend/len (2026-09-08) — 개념 설명은 README.md 참고"""

# 기능: 기존 데이터에 값 추가 -> append() 함수
list_data = [0, 1, 2, 3, 4]
print(f"데이터 추가 전 리스트 자료형: {list_data}")

print("-" * 80)

# 목표: 마지막 위치에 5를 추가
list_data.append(5)
print(f"데이터 추가 후 리스트 자료형: {list_data}")

# 여러 개를 동시에 추가하는 세 가지 방법
cart1 = []
print(f"데이터 추가 전 리스트 자료형: {cart1}")

print("-" * 80)

# 방법1: append() -> 순차적으로 추가 (동시 추가는 불가능)
cart1.append("계란")
print(f"데이터 추가 후 리스트 자료형: {cart1}")
cart1.append("우유")
print(f"데이터 추가 후 리스트 자료형: {cart1}")
cart1.append("사과")
print(f"데이터 추가 후 리스트 자료형: {cart1}")

print("-" * 80)

# 방법2: extend() -> 작은 리스트를 연결해서 긴 리스트 1개 생성
cart2 = []
foods = ["계란", "우유", "사과"]
cart2.extend(foods)
print(f"리스트 데이터를 추가한 결과: {cart2}")

print("-" * 80)

# 방법3: 덧셈 연산자 -> 작은 리스트를 연결해서 긴 리스트 1개 생성
cart3 = []
foods = ["계란", "우유", "사과"]
output = cart3 + foods
print(f"덧셈 연산자를 이용하여 두 리스트를 연결한 결과: {output}")

# 성분 원소의 개수 확인 -> len() 함수 -> 범용 함수
list_data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
counts = len(list_data)
print(f"리스트 자료형 데이터 안에 들어있는 성분 원소의 개수: {counts}")