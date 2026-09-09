"""TIL: 반복문 for/while 기본 (2026-09-09) — 개념 설명은 README.md 참고"""

# for 반복문 실습(1) - 리스트
list_food = ["햄버거", "치킨", "피자"]

for food in list_food:
    # print(food)
    print("Hi")

# for 반복문 실습(2) - 문자열
string = "안녕하세요"

for data in string:
    print(data)
    print("Hi")

# for 반복문 실습(3) - range() 함수
numbers = range(0, 100)
print(numbers)

print("-" * 80)

for number in range(0, 100):
    print(f"Hi{number}")

# while 반복문 - 조건이 참인 동안 반복
count = 1

while count <= 5:
    print(count)
    count += 1

# while True + break - 무한 루프 + 종료 조건
while True:
    user_input = input("사용자: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    else:
        print(f"사용자 입력값: {user_input}")