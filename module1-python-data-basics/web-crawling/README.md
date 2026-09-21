# Module 1 - Open API & 웹크롤링 데이터 수집

## 📅 2026-09-18 | Open API 데이터 수집 - 개념 · requests 활용 · MySQL 저장
> 코드: [`api_basics.py`](./api_basics.py), [`collect_popular_books.py`](./collect_popular_books.py), [`book_table.sql`](./book_table.sql)

### 개념

**1. 데이터 수집 방법 2가지**
- Open API: 서비스 업체가 제공하는 규칙대로 데이터를 요청/응답받는 방식
- Web 크롤링(crawling): 웹 페이지에서 직접 정보를 추출하는 방식

**2. API(Application Programming Interface)**
- 서로 다른 컴퓨터 프로그램끼리 대화할 수 있게 돕는 메신저이자 통신 규칙
- 반드시 서비스 업체가 제공하는 규칙(API 매뉴얼)대로 구현·실행해야 함
- 종류
  - REST API(웹 API): 인터넷을 통해 요청, URL 작성 필요
  - 라이브러리 API: 함수 형태 (예: `print()`)
- 공개 범위에 따른 분류
  - Private API(비공개 API): 조직 내에서만 사용 가능
  - 오픈 API: 누구나 사용 가능

**3. JSON (JavaScript Object Notation)**
- 서버와 클라이언트가 데이터를 주고받을 때 쓰는, 키-값 쌍으로 이루어진 텍스트 기반 표준 형식
- Python dict와 구조는 같지만(`{key: value}`), JSON은 **문자열(string) 자료형**이고 python dict는 **dict 자료형**
- JSON 문자열 → python dict 변환: `json.loads(json_string)`

**4. requests 라이브러리로 API 호출하기**
- 설치: `pip install requests`
- 사용법: `requests.get(url).text` → JSON 문자열 형태로 응답 수신
- 호출 URL 구성: `기본URL?파라미터1=값1&파라미터2=값2` (기본URL과 파라미터는 `?`로, 파라미터끼리는 `&`로 연결)

**5. 도서관 정보나루 API 실습 과정**
- 회원가입 → API 인증키 발급 → 매뉴얼에서 원하는 API(인기대출도서 조회) 확인 → 호출 URL 작성 → 데이터 수집
- 주요 파라미터: `authKey`(인증키), `startDt`/`endDt`(검색 기간), `age`(연령대), `format=json`(응답 형식)

**6. JSON 데이터에서 원하는 정보 추출하기**
- 중첩된 딕셔너리 구조를 `.get()`으로 한 단계씩 파고들어 접근
  (`dict_data.get("response").get("docs")`처럼 체이닝)
- 추출한 데이터를 `pandas.DataFrame()`으로 표 형태로 변환 → `.to_csv(file_path)`로 CSV 저장

**7. 생성형 AI 활용 프롬프트 작성 원칙**
- 역할 부여 및 규칙 설정: "너는 경력 O년 이상의 O 전문가야. ~는 되고 ~는 안 돼" 형태로 페르소나·제약 명시
- 요청을 매우 구체적으로 전달: 실습 환경, 원하는 결과, 과정, 기술적 세부사항까지 포함

**8. Open API 수집 데이터의 MySQL 저장**
- CSV 파일의 데이터 구조·컬럼 타입을 분석해서 최적의 테이블(DDL) 설계
- MySQL Workbench의 Table Data Import Wizard로 CSV → 테이블 적재 (CSV 헤더와 DB 컬럼 1:1 매핑)
- `DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`: DB 생성 시 이모지/다국어 지원 설정

### 왜 이렇게 코딩했는가
- API 인증키를 코드에 직접 문자열로 적지 않고 `.env` 파일 + `os.getenv()`로 분리한 이유
  → 인증키가 그대로 코드에 노출되면, 깃허브 등에 공유했을 때 다른 사람이 내 키를 가져다 쓸 수 있어서 보안상 위험함. `.env`는 `.gitignore`로 커밋 대상에서 제외해서 실제 키가 외부에 노출되지 않도록 함
- 생성형 AI에게 코드를 요청할 때 API 매뉴얼 이미지를 직접 첨부하고, 실습 환경(OS, 가상환경 이름)까지 구체적으로 명시한 이유
  → AI가 추측이 아니라 실제 API 명세에 정확히 맞는 코드를 생성하도록, 그리고 내 개발 환경에서 바로 실행 가능한 코드를 받기 위함
- `response.raise_for_status()`와 `try-except`로 API 호출을 감싼 이유
  → 네트워크 오류나 API 응답 실패 시 프로그램이 그냥 죽지 않고, 원인을 파악할 수 있는 에러 메시지를 출력하도록 지난번 배운 예외 처리를 적용함
- `book_table`을 만들 때 `testdb`가 아니라 `bookdb`라는 별도 데이터베이스로 분리한 이유
  → 도서 데이터라는 주제가 명확한 데이터셋이라, 이것저것 섞인 `testdb`보다 목적이 분명한 별도 DB로 관리하는 게 나중에 찾기 편함
- 컬럼 타입을 `INT` 대신 `INT UNSIGNED`(순위, 대출건수처럼 음수가 없는 값), `pub_year`를 `YEAR` 타입으로 지정한 이유
  → 데이터의 실제 의미에 맞는 타입을 써서, 음수가 들어갈 수 없는 값은 애초에 음수 저장을 막고(UNSIGNED), 연도만 필요한 컬럼은 불필요하게 큰 DATETIME 대신 가벼운 YEAR 타입을 사용함

### 막혔던 부분 / 이해 포인트
- API 응답으로 받은 JSON 구조가 `response > docs > doc > {실제 데이터}`처럼 여러 겹으로 중첩되어 있어서, `.get()`을 여러 번 이어 붙여야 원하는 데이터에 도달할 수 있다는 걸 확인함
  → `dict_data.keys()`로 한 단계씩 구조를 확인해가며 어디까지 파고들어야 하는지 파악하는 방식이 도움이 됨
- CSV로 저장한 데이터를 MySQL에 그대로 넣으려 하면 컬럼 타입이 안 맞을 수 있어서, Import 전에 CSV 컬럼 구조를 보고 미리 적절한 테이블(DDL)을 설계해둬야 한다는 걸 이해함

---

## 📅 2026-09-21 | 웹크롤링 - HTML/CSS 기초, 정적 크롤링(BeautifulSoup), 동적 크롤링(Selenium)
> 코드: [`selenium_book_pages.py`](./selenium_book_pages.py), ['kurly_review_crawler.py'](./kurly_review_crawler.py), ['seoul_commercial_data.py'](./seoul_commercial_data.py)

### 개념

**1. 크롤링(crawling)이란**
- 웹 페이지의 정보를 자동화된 방법으로 수집하고 데이터를 추출하여 저장하는 기술
- 종류: 정적 크롤링(고정된 데이터), 동적 크롤링(상호작용으로 변하는 실시간 데이터)

**2. HTML 기본 구조**
- `<!DOCTYPE html>`: HTML5 표준 형식 선언
- `<html>`: 문서의 시작과 끝, 내부를 `<head>`와 `<body>`로 나눔
- `<head>`: 사용자 눈에 안 보이는 부가 정보(metadata)
- `<body>`: 브라우저에 실제로 표시되는 모든 콘텐츠
- 태그 구조: `<태그이름>콘텐츠</태그이름>` (시작 태그 + 종료 태그가 콘텐츠를 감쌈)

**3. 주요 HTML 태그**
- `a`: 하이퍼링크, `href` 속성으로 이동할 주소 지정
- `h1~h6`: 제목(Heading), 숫자가 작을수록 큰 제목
- `ul`/`ol`/`li`: 순서 없는/있는 목록과 개별 항목, `br`: 줄바꿈
- `table`/`tr`/`th`/`td`: 표(행/제목/데이터)
- `div`: 여러 태그를 묶는 컨테이너 (자체로는 시각적 변화 없음, CSS와 함께 그룹 스타일링에 사용)

**4. id / class 속성**
- id: 고유 식별자, 중복 사용 불가 (`#id`)
- class: 그룹 식별자, 여러 태그에 중복 적용 가능 (`.class`)

**5. CSS**
- HTML 문서를 다양한 스타일로 디자인하는 언어, id/class를 이용해 특정 요소를 선택

**6. 정적 크롤링 — BeautifulSoup**
- HTML 문서를 파싱(구조화)해서 원하는 데이터를 쉽게 추출하는 라이브러리
- 파싱: HTML 코드를 분석해 계층적(나무 구조) 형태로 표현하는 것
- 사용법: HTML 가져오기(`requests`) → `BeautifulSoup(html, "html.parser")`로 분석 → `soup.select("CSS 선택자")`로 원하는 태그 찾기 → `.text`/`.get_text()`로 텍스트 추출
- CSS 선택자 종류: 태그 선택자(`p`), 클래스 선택자(`.box`), 아이디 선택자(`#header`)

**7. 동적 크롤링 — Selenium**
- 실제 브라우저를 자동으로 조작해서 상호작용이 필요한 데이터(무한 스크롤, 클릭해야 열리는 내용 등)까지 수집
- 개발자 도구(F12)의 "요소 선택 아이콘"으로 원하는 정보의 HTML 위치 확인 → 마우스 우클릭 → Copy → **Copy selector**로 CSS 선택자 주소 복사
- Selenium 핵심 3단계
  1. `driver = webdriver.Chrome()`: 자동 조작할 브라우저(아바타 브라우저) 생성
  2. `driver.get(url)`: 원하는 페이지로 이동
  3. `driver.find_element(By.CSS_SELECTOR, selector)`: 요소 찾기 → `.text`로 정보 추출

### 왜 이렇게 코딩했는가
- 마켓컬리 리뷰 수집 코드에서 `--disable-blink-features=AutomationControlled`, User-Agent 직접 지정,
  `navigator.webdriver` 속성 재정의 같은 "봇 탐지 우회" 설정을 프롬프트에 명시적으로 요청한 이유
  → 많은 쇼핑몰 사이트가 자동화 도구(Selenium)로 접속하는 걸 감지해서 차단하는데, 실제 사람이
    사용하는 것처럼 보이도록 설정하지 않으면 페이지 자체가 제대로 안 열리거나 데이터가 비어있는
    상태로 나올 수 있어서 미리 방지 조치를 요청함
- 다음 페이지 버튼을 클릭할 때 `.click()` 대신 `driver.execute_script("arguments[0].click();", next_btn)`으로
  JS(자바스크립트)를 직접 실행해 클릭한 이유
  → 일반 `.click()`은 다른 요소가 버튼을 가리고 있으면 `ElementClickInterceptedException` 에러가
    나는 경우가 있는데, JS로 직접 클릭 이벤트를 실행하면 화면에 다른 요소가 겹쳐 있어도 우회해서
    클릭할 수 있음
- 서울시 공공데이터 수집 코드에서 API 요청을 1,000건씩 나눠서(`PAGE_SIZE`) 반복 호출한 이유
  → 공공 API는 보통 한 번에 가져올 수 있는 데이터 건수에 제한(1회 최대 1,000건)이 있어서,
    전체 데이터가 그보다 많으면 시작/끝 인덱스를 바꿔가며 여러 번 나눠서 요청해야 함
- API 표기 건수, 파이썬에서 실제로 수집한 건수, CSV로 저장한 후 다시 읽어들인 건수, 이 세 가지를
  전부 비교하는 "삼중 검증"을 넣은 이유
  → 수집 과정 중 일부 데이터가 누락되거나, 저장 과정에서 인코딩 문제로 깨지는 경우를 놓치지 않고
    확인하기 위해, 각 단계마다 건수가 정확히 일치하는지 교차 검증함

### 이해 포인트
- 동적 크롤링은 대상 사이트가 봇 탐지를 하는 경우, 단순히 `webdriver.Chrome()`만으로는 데이터를
  못 가져올 수 있다는 걸 확인함 (실제 브라우저처럼 보이게 하는 추가 설정이 필요함)
- 공공 API처럼 데이터가 아직 존재하지 않는 분기(예: 아직 지나지 않은 미래 분기)를 요청하면 정상
  응답이 아니라 별도의 상태 코드(`INFO-200` 등)가 와서, 이런 경우를 에러로 처리하지 않고 "데이터
  없음"으로 구분해서 처리해야 한다는 걸 확인함
- CSV로 저장만 하고 끝내는 게 아니라, 저장한 파일을 다시 읽어들여서 건수를 재확인하는 방식으로
  "진짜로 파일이 제대로 저장됐는지"까지 검증할 수 있다는 걸 배움

---

