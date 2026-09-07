"""TIL: 문자열(str) - 생성/인덱싱/슬라이싱/연결 (2026-09-07) — 개념 설명은 README.md 참고"""

# 여러 줄 문자열 생성
multi_line = """
This is line number1.
this is line number2.
this is line number3.
this is lien number4.
"""
print(f"여러 줄 문자열 생성의 결과 : {multi_line}")

# 인덱싱과 슬라이싱
string = "문자열은 인덱싱과 슬라이싱이 가능하다."
print(string)
print("-" * 80)

first_element_str = string[0]
print(f"첫 번째 글자 : {first_element_str}")
print("-" * 80)

last_element_str = string[-1]
print(f"마지막 글자 : {last_element_str}")
print("-" * 80)

string1 = string[0:5]
print(f"처음부터 다섯 번째 글자까지 슬라이싱 결과 : {string1}")

# 문자열 연결하기
string1 = "Good"
string2 = "Morning!"
output = string1 + " " + string2
print(f"문자열 연결의 결과 : {output}")

# 문자열 반복 (곱셈 연산자)
output2 = string2 * 3
print(output2)

output3 = "-" * 80
print(output3)