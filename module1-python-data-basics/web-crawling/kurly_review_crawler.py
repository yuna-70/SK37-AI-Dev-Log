"""TIL: 생성형 AI 활용 동적 크롤링 - 마켓컬리 리뷰 수집 (봇 탐지 우회) (2026-09-21) — 개념 설명은 README.md 참고"""

import os
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def create_robust_driver():
    """크롬 드라이버의 봇 탐지 방지(Anti-Bot) 강력 설정 적용"""
    chrome_options = Options()

    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    user_agent = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    )
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--lang=ko_KR")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined });"},
    )

    return driver


def crawl_kurly_reviews():
    target_url = "https://www.kurly.com/goods/5026468"
    max_pages = 20
    data_list = []

    driver = create_robust_driver()
    wait = WebDriverWait(driver, 15)

    try:
        print(f"[안내] 수집 대상 URL 접속 중: {target_url}")
        driver.get(target_url)
        time.sleep(random.uniform(2.5, 3.5))

        # 1. 상품명 수집
        product_name = "상품명 미상"
        try:
            product_elem = wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "h3.css-1dvwoi6, h3[class*='e6cseyw2'], h1.goods-name")
                )
            )
            product_name = product_elem.text.strip()
            print(f"[성공] 수집 대상 상품명: {product_name}")
        except Exception as e:
            print(f"[경고] 상단 상품명을 찾을 수 없어 기본 선택자를 시도합니다: {e}")

        # 2. 리뷰 섹션까지 스크롤 이동
        print("[안내] 리뷰 섹션으로 페이지 스크롤 진행...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1.5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(1.5)

        # 3. 1페이지부터 20페이지까지 리뷰 데이터 수집
        for current_page in range(1, max_pages + 1):
            print(f"\n>>> 현재 {current_page} 페이지 수집 중...")
            time.sleep(random.uniform(1.5, 2.5))

            review_elements = driver.find_elements(By.CSS_SELECTOR, "p.css-y49dcn, p[class*='e6cseyw1']")
            date_elements = driver.find_elements(By.CSS_SELECTOR, "span.css-14kcwq8, span[class*='e6cseyw14']")

            count_in_page = min(len(review_elements), len(date_elements))
            print(f"   - {current_page}페이지 발견된 리뷰 건수: {count_in_page}개")

            for i in range(count_in_page):
                r_text = review_elements[i].text.strip().replace("\n", " ")
                d_text = date_elements[i].text.strip()
                if r_text and d_text:
                    data_list.append({"상품명": product_name, "날짜": d_text, "리뷰": r_text})

            if current_page < max_pages:
                try:
                    next_buttons = driver.find_elements(By.CSS_SELECTOR, "button.css-frxx9h, button[class*='e8bfz7t3']")
                    if not next_buttons:
                        print("[안내] 다음 페이지 버튼을 찾을 수 없어 수집을 종료합니다.")
                        break

                    next_btn = next_buttons[-1]
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", next_btn)
                    time.sleep(0.8)
                    driver.execute_script("arguments[0].click();", next_btn)
                    print(f"   - {current_page + 1} 페이지로 이동 버튼 클릭 완료")

                except Exception as ex:
                    print(f"[오류] {current_page} 페이지에서 다음 페이지 이동 중 예외 발생: {ex}")
                    break

        # 4. CSV 저장
        if data_list:
            df = pd.DataFrame(data_list)
            df = df[["상품명", "날짜", "리뷰"]]
            output_file = "kurly_product_reviews.csv"
            df.to_csv(output_file, index=False, encoding="utf-8-sig")

            print("\n" + "=" * 60)
            print(f"[수집 완료] 총 {len(df)}건의 리뷰 데이터가 저장되었습니다.")
            print(f"[저장 경로] {os.path.abspath(output_file)}")
            print("=" * 60)
        else:
            print("[경고] 수집된 데이터가 없습니다.")

    except Exception as e:
        print(f"[최상위 오류 발생] {e}")

    finally:
        driver.quit()
        print("[안내] 브라우저를 정상 종료했습니다.")


if __name__ == "__main__":
    crawl_kurly_reviews()