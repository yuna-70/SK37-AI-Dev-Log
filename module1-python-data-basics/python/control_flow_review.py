"""TIL: 제어문 종합 복습 6문제 (2026-09-09) — 개념 설명은 README.md 참고"""

# 문제 1
# [if-else 조건문을 활용한 온도 판별]
# 변수 temperature에 28을 저장한 후, if-else문을 사용하여 온도가 25 이상이면 "에어컨 작동",
# 그렇지 않으면 "에어컨 정지"를 출력하는 코드를 작성하세요.
temperature = 28
if temperature >= 25:
    print("에어컨 작동")
else:
    print("에어컨 정지")

# 문제 2
# [if-elif-else 조건문을 활용한 연령대 구분]
# 변수 age에 15를 저장한 후, 다음 조건에 따라 연령대를 분류하여 출력하는 코드를 작성하세요.
# - 19세 이상: "성인"
# - 13세 이상 19세 미만: "청소년"
# - 13세 미만: "어린이"
age = 15
if age >= 19:
    print("성인")
elif age >= 13:
    print("청소년")
else:
    print("어린이")

# 문제 3
# [for문과 range() 함수를 활용한 반복 출력]
# for문과 range() 함수를 사용하여 1부터 5까지의 숫자를 f-string을 활용해
# "현재 번호: 1" ~ "현재 번호: 5" 형식으로 출력하는 코드를 작성하세요.
for number in range(1, 6):
    print(f"현재 번호: {number}")

# 문제 4
# [while 반복문과 카운터 변수 활용]
# 카운터 변수 count = 1을 생성하고, while 조건식을 이용하여 count가 3 이하인 동안
# "파이썬 재밌다!"를 출력하고 count를 1씩 증가시키는 코드를 작성하세요.
count = 1
while count <= 3:
    print("파이썬 재밌다!")
    count += 1

# 문제 5
# [while True 무한 루프와 break 탈출]
# num = 1 변수를 설정한 후, while True: 무한 루프 안에서 num 값을 출력하세요.
# num이 4와 같아지면 "반복 종료"를 출력하고 break문으로 루프를 탈출하는 코드를 작성하세요
# (단, 매 반복마다 num을 1씩 증가시킵니다).
num = 1
while True:
    print(num)
    if num == 4:
        print("반복 종료")
        break
    num += 1

# 문제 6
# [for 반복문 + 리스트 + if-else 조건문 융합]
# 도시 이름이 담긴 리스트 cities = ["서울", "부산", "대구", "인천"]이 있습니다. for문으로 리스트의
# 각 도시를 순회하면서, 도시 이름이 "서울"이면 "수도: 서울"을 출력하고, 그렇지 않으면
# f-string을 활용해 "지방: [도시명]"을 출력하는 코드를 작성하세요.
cities = ["서울", "부산", "대구", "인천"]
for city_name in cities:
    if city_name == "서울":
        print(f"수도: {city_name}")
    else:
        print(f"지방: {city_name}")