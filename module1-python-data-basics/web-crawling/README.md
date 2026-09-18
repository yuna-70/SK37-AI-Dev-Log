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