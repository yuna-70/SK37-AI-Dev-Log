"""TIL: 모듈/패키지/라이브러리 - random, requests (2026-09-11) — 개념 설명은 README.md 참고"""

# 내장 모듈 - 목표: random 모듈을 이용한 로또 번호 추출
from random import sample

numbers = range(1, 46)
lottery_list = []

for num in range(1, 6):
    lottery = sample(numbers, 6)
    lottery_list.append(lottery)

print(lottery_list)

# 외부 라이브러리 - 목표: 구글 웹페이지 HTML 가져오기
import requests

url = "https://www.google.com"
output = requests.get(url=url)
html = output.text
print(html)