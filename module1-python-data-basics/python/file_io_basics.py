"""TIL: 파일 처리 - 읽기(read/readlines) / 쓰기(write) (2026-09-10) — 개념 설명은 README.md 참고"""

# 파일 읽기 - with open + read() / readlines()
file_path = "python.txt"

with open(file_path, "r") as f:
    text = f.read()
    print(text)
    print("-" * 80)

print(f"text 내부의 글자 수 : {len(text)}개")

print("-" * 80)

with open(file_path, "r") as f:
    text_list = f.readlines()
    print(text_list)
    print("-" * 80)

print(f"text_list의 요소 수 : {len(text_list)}개")

# 파일 쓰기 - with open + write()
file_path = "count_log.txt"

with open(file=file_path, mode="w", encoding="utf-8") as f:
    for num in range(1, 11):
        data = f"{num}번째 줄입니다.\n"
        f.write(data)