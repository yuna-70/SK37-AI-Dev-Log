"""TIL: 문자열 전용 함수 - capitalize/upper/lower/title/split/join/replace/strip (2026-09-08) — 개념 설명은 README.md 참고"""

# capitalize() - 첫 글자만 대문자로
string = "python"
output = string.capitalize()
print(output)

# upper() - 전체 대문자로
string = "python"
output = string.upper()
print(output)

# lower() - 전체 소문자로
string = "PYTHON"
output = string.lower()
print(output)

# title() - 각 단어 첫 글자만 대문자로
string = "python just do it"
output = string.title()
print(output)

# split() - 기준 문자로 문자열 분리 -> 리스트 반환
string1 = "zero one two three"
output1 = string1.split()  # 기본값: 공백 기준
print(output1)

print("-" * 80)

string2 = "python, jquery, javascript"
output2 = string2.split(",")  # 쉼표 기준
print(output2)

# join() - 리스트를 기준 문자로 연결
colors = ["red", "blue", "green", "yellow"]
output = " ".join(colors)
print(output)

print("-" * 80)

output2 = ", ".join(colors)
print(output2)

# replace() - 특정 문자(열) 치환
string = "Life is too short."
print(f"replace 함수 사용 전 문자열: {string}")

print("-" * 80)

output = string.replace("Life", "My Leg")
print(f"replace 함수 사용 후 문자열: {output}")

# strip() - 시작/끝 공백, 줄바꿈 제거
string = "\n\n Hello world, Python! \n"
print(f"strip 함수 사용 전 문자열 출력: \n{string}")

print("-" * 80)

output = string.strip()
print(f"strip 함수 사용 후 문자열 출력: \n{output}")