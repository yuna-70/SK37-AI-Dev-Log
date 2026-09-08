"""TIL: 사용자 정의 함수 - 정의와 호출 (2026-09-08) — 개념 설명은 README.md 참고"""

# 사용자 정의 함수로서 덧셈 함수 정의
def add(x, y):
    sum = x + y
    return sum

# 함수 호출 + 인수(argument) 입력(1) - 위치 인수
output1 = add(3, 5)
print(output1)

print("-" * 80)

# 함수 호출 + 인수(argument) 입력(2) - 키워드 인수
output2 = add(x=3, y=5)
print(output2)