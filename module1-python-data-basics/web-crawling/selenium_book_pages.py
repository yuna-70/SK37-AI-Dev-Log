"""TIL: Selenium 동적 크롤링 - 교보문고 도서 쪽수 정보 수집 (2026-09-21) — 개념 설명은 README.md 참고"""

from selenium import webdriver
from selenium.webdriver.common.by import By

# Chrome 브라우저를 자동 조작하기 위한 '아바타 브라우저' 생성
driver = webdriver.Chrome()

# 이동하고 싶은 웹사이트 주소: 교보문고, 물고기는 존재하지 않는다
url = "https://product.kyobobook.co.kr/detail/S000001925800"

try:
    # 페이지 이동
    driver.get(url)

    # F12로 복사한 selector 주소
    selector = "div.flex.flex-wrap.items-center.gap-2 > span"

    # selector 주소에 해당하는 '요소(element)'를 찾아서 변수에 저장
    element = driver.find_element(By.CSS_SELECTOR, selector)

    # 찾은 요소에서 text 추출
    page_info = element.text.split(" |")[0]

    print(f"도서 쪽수: {page_info}")

except Exception as e:
    print(f"에러 발생: {e}")