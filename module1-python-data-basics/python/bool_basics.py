"""TIL: 불리언(Boolean) - 값/기능/숫자 취급 특징 (2026-09-07) — 개념 설명은 README.md 참고"""

# 크기 비교 -> 긍정/부정 표시
money = 10000
output1 = (money > 100000)
print(f"크기 비교의 결과 : {output1}")

output2 = (1 % 2 == 1)
print(f"크기 비교의 결과 : {output2}")

# 불리언 자료형의 특징: 연산 시 숫자로 인식
bool_data1 = True
print(bool_data1)
print("-" * 80)

bool_data2 = False
print(bool_data2)

sum = bool_data1 + bool_data2 + bool_data1
print(f"덧셈 연산의 결과 : {sum}")

print("-" * 80)

sub = bool_data1 - 3
print(f"뺄셈의 결과 : {sub}")