"""TIL: 숫자형 자료형 - 생성/연산/조건 판별 (2026-09-07) — 개념 설명은 README.md 참고"""

# 숫자형 데이터 생성
num1 = 123
print(f"정수형 데이터 : {num1}")

num2 = 1.2
print(f"실수형 데이터 : {num2}")

# 사칙 연산
output1 = num1 + num2
print(output1)

output2 = num1 - num2
print(output2)

output3 = num1 * num2
print(output3)

output4 = num1 / num2
print(output4)

# 제곱 연산 (3의 4제곱)
num1 = 3
num2 = 4
output = num1 ** num2
print(f"3의 4제곱 : {output}")

# 나머지 연산
print(7 % 3)

# 짝수, 홀수 구별
print(2 % 2)
print(2 % 2 == 0)  # 짝수

print(1 % 2)
print(1 % 2 == 1)  # 홀수

# 배수 구별 (5의 배수)
print(15 % 5)
print(15 % 5 == 0)

# 몫 연산
print(7 // 3)