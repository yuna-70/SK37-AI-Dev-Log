## 📅 2026-09-15 | Database 기초 - 개념 · DB/테이블 생성 · CRUD · 조회 필터링
> 코드: [`sql/db_table_basics.sql`](./db_table_basics.sql), [`sql/crud.sql`](./crud.sql), [`sql/query_filter.sql`](./query_filter.sql)

### 개념

**1. 데이터베이스(DB)와 DBMS**
- 데이터베이스: 컴퓨터로 저장·관리하는 데이터의 집합
- DBMS: 데이터베이스를 운영·관리하는 소프트웨어 (MySQL, MariaDB, PostgreSQL, Oracle, SQLite)
- 관계형 DBMS: 정보를 표(table) 형식으로 저장, 테이블은 레코드(행)와 필드(열)로 구성
- 데이터베이스는 폴더 구조이며, 그 안에 테이블이 파일 형태로 저장됨

**2. 엑셀 vs 데이터베이스**
- 데이터베이스 장점: 여러 사용자·프로그램이 동시 접근 가능, 데이터가 안전하게 저장·보호됨
- 단점: 복잡해서 전문가(관리자)가 필요함

**3. MySQL**
- 오픈소스 기반의 가장 인기 있는 관계형 DBMS(RDBMS), 뛰어난 성능·신뢰성·사용성
- Community Edition(무료, 본 과정 실습 버전) vs Enterprise Edition(유료)

**4. 정보시스템 구축 5단계 (SDLC)**
- 요구사항 분석 → 시스템 설계(ERD 작성, 핵심) → 프로그램 구현(테이블 생성·코딩) → 테스트 → 유지보수

**5. 모델 / 모델링 / ERD**
- 관계형 DB는 데이터 중복을 막기 위해 정보를 여러 테이블로 세분화(정규화)함
  - 예: 주문 테이블에 회원·상품 정보를 다 넣으면 중복·불일치(예: 주소 변경 시 일부 행만 수정되는 문제) 발생 → 회원/상품/주문 테이블로 분리
- 모델(결과물): 데이터 구조의 틀, 실체는 테이블 + 테이블 정의서
- 모델링(과정): 요구사항을 모델로 변환하는 전체 프로세스 (테이블 분리, PK 결정, 관계 설정 등)
- ERD(시각화 설계도): 테이블 구조와 관계를 그림으로 표현 (테이블=네모, 컬럼명·자료형 명시, 관계는 선과 기호)

**6. DB 모델링 필수 용어**
- 엔티티: 관리하고자 하는 대상(명사) → 테이블이 됨 (테이블 = 모델 = 엔티티)
- 속성: 엔티티의 세부 특징 → 테이블의 컬럼이 됨
- 관계: 엔티티 간 연관성(동사로 표현), 1:1 / 1:N / N:M 세 가지
  - 1:1 (국민 1명 - 주민등록증 1개) / 1:N (부서 1개 - 사원 여러 명) / N:M (회원 여러 명 - 상품 여러 개, 서로 다대다)
- 주식별자(PK): 행 하나를 유일하게 구별하는 대표 속성 (학번, 회원ID 등)

**7. 데이터베이스 모델링 3단계**
- 개념적 모델링: 핵심 Entity·Relationship 추출 → ERD(그림)로 표현
- 논리적 모델링: ERD를 테이블 형태로 변환, 속성·PK 정의
- 물리적 모델링: 실제 DBMS(MySQL) 특성에 맞춰 구체적 데이터 형식(INT 등) 지정

**8. SQL 명령어 분류**
- DDL(데이터 정의어): DB·테이블 등 스키마를 생성·변경·삭제
- DML(데이터 조작어): 테이블 내 실제 데이터를 조회·입력·수정·삭제

**9. 제약조건**
- PRIMARY KEY: 행을 유일하게 식별 (테이블당 1개), Unique + NOT NULL 자동 보유
- NOT NULL: NULL 값 금지, 데이터 무결성 보장
- AUTO_INCREMENT: 정수형 PK 컬럼에 사용, 행 추가 시 1씩 자동 증가 (테이블당 1개만 설정 가능)
- FOREIGN KEY: 한 테이블의 컬럼이 다른 테이블의 PK를 참조 (부모-자식 관계 형성)
  - 참조 무결성: 자식 테이블은 부모 테이블 PK에 실제 존재하는 값만 가질 수 있음

**10. WHERE 절과 연산자**
- 비교 연산자: `=`, `!=`, `>`, `<`, `>=`, `<=`
- 논리 연산자: `AND`(둘 다 참), `OR`(하나라도 참), `NOT`(부정)

**11. 범위·목록·패턴 검색**
- `BETWEEN A AND B`: A 이상 B 이하 연속 범위
- `IN (값1, 값2, ...)`: 목록 중 하나라도 일치
- `LIKE` + 와일드카드: `%`(글자 수 제한 없음), `_`(정확히 그 자리 수만큼)

### 왜 이렇게 코딩했는가
- 종합 실습(회원 DB)에서 `INSERT`할 때 3건을 한 번에 쉼표로 나열해서 입력한 이유
  → 같은 테이블에 여러 행을 넣을 때 `INSERT`문을 3번 따로 실행하지 않고 한 번에 처리하기 위함
- `DROP TABLE IF EXISTS test_table;`처럼 `IF EXISTS`를 붙인 이유
  → 해당 테이블이 없을 때 `DROP TABLE`만 실행하면 에러가 나는데, `IF EXISTS`를 붙이면 테이블이 없어도 에러 없이 넘어가서 실습을 반복 실행하기 안전함

### 이해 포인트
- `UPDATE`/`DELETE`를 `WHERE` 절 없이 실행하거나, PK가 아닌 조건으로 수정하려 하면 MySQL의 Safe Mode가 이를 막는다는 걸 확인함
  → `SET sql_safe_updates = 0;`으로 Safe Mode를 해제해야 조건 없는 일괄 수정이 가능함
- `SET Name = "값"`처럼 SQL도 파이썬처럼 대입 연산자(`=`) 앞뒤로 띄어쓰는 게 일반적인 스타일이라는 걸 확인함

---

## 📅 2026-09-16 | 집계함수·GROUP BY·UPSERT·형변환·내장함수·JOIN 시작
> 코드: [`aggregate_groupby.sql`](./aggregate_groupby.sql), [`upsert.sql`](./upsert.sql), [`variables_casting.sql`](./variables_casting.sql), [`functions.sql`](./functions.sql), [`join.sql`](./join.sql) (`query_filter.sql`에 조건별 조회 실습 2개 추가)

### 개념

**1. 집계 함수 (SUM, AVG, COUNT, MAX, MIN)**
- 여러 행의 데이터를 입력받아 단 하나의 요약된 결과값을 계산하는 함수
- NULL 값은 자동으로 계산 대상에서 제외됨

**2. GROUP BY**
- 특정 컬럼의 값이 같은 데이터끼리 묶어서 그룹별 집계 통계를 낼 때 사용 (Pandas의 `groupby`와 같은 기능)

**3. WHERE vs HAVING**
- WHERE: 개별 행 단위의 1차 필터링, 집계 함수 사용 불가, 그룹으로 묶기 **전** 필터링
- HAVING: 그룹화된 결과에 대한 2차 필터링, 그룹으로 묶은 **후** 집계 결과 기준 필터링
- 둘을 함께 쓸 수도 있음: `WHERE`로 먼저 개별 행을 거른 뒤 `GROUP BY`로 묶고, `HAVING`으로 그룹 결과를 한 번 더 거르는 조합

**4. 조건부 데이터 입력/수정 (UPSERT)**
- `INSERT IGNORE`: PK 중복 에러 발생 시 에러 무시하고 해당 행 삽입을 건너뜀
- `ON DUPLICATE KEY UPDATE`: PK 중복이 없으면 신규 삽입, 중복되면 지정한 값으로 자동 수정

**5. 사용자 정의 변수 (@변수)**
- 세션이 유지되는 동안 프로그램 전체에서 값을 기억하는 변수
- 사용법: `SET @변수명 = 값;` → 쿼리 안에서 `@변수명`으로 참조

**6. 명시적/묵시적 형변환**
- 명시적(Explicit): `CAST(값 AS 타입)` / `CONVERT(값, 타입)`으로 개발자가 직접 변환
  - 주의: 형변환 함수 안에서는 테이블 생성용 타입(INT, VARCHAR, FLOAT)이 아니라 전용 타입을 써야 함
    (정수 → `SIGNED`/`UNSIGNED`, 문자열 → `CHAR`, 실수 → `DECIMAL`)
- 묵시적(Implicit): 형변환 함수 없이 연산자/문맥에 따라 MySQL이 자동으로 타입 변환
  - `'100' + '200'`처럼 숫자로 변환 가능한 문자열은 자동 계산되지만, `'a' + 'B'`처럼 변환 불가능하면 0으로 처리됨(에러 없이)
  - 문자열을 "연결"하려면 `+`가 아니라 `CONCAT()`을 써야 함

**7. 주요 내장 함수**
- 문자열: `CONCAT`(연결), `SUBSTRING`(부분 추출), `LENGTH`/`CHAR_LENGTH`, `LOWER`/`UPPER`, `REPLACE`
- 날짜: `NOW()`, `CURDATE()`, `CURTIME()`, `DATEDIFF`, `DATE_ADD`, `DATE_FORMAT`
- 제어 흐름: `IF(조건, 참값, 거짓값)`, `IFNULL(값, 대체값)`, `CASE WHEN ... THEN ... ELSE ... END`
  - CASE는 위에서부터 순차 평가, 가장 먼저 참이 되는 조건의 결과 반환, ELSE 생략 시 미충족 시 NULL 반환
- NULL 처리: `IS NULL` / `IS NOT NULL`
  - NULL은 "값이 없음/알 수 없음"이라 `=`, `!=` 같은 일반 비교 연산자로 비교 불가, 반드시 `IS`로 확인
- `LIKE`와 `IN`의 차이: `LIKE`는 와일드카드(`%`, `_`)를 활용한 **부분 일치** 검색, `IN`은 지정한 목록 중 **완전 일치**하는 값만 찾음

**8. 조인(JOIN)**
- 여러 테이블에 나뉘어 저장된 데이터를 공통 컬럼(PK-FK)을 매개로 하나로 합쳐 조회하는 기술
- 종류
  - INNER JOIN: 두 테이블 모두에 존재하는 교집합만 결합
  - LEFT/RIGHT OUTER JOIN: 한쪽 테이블 기준 전체 + 매칭 데이터 결합
  - CROSS JOIN: 모든 경우의 수 조합(카테시안 곱)
  - SELF JOIN: 자기 자신과의 조인 (조직도 등)

### 왜 이렇게 코딩했는가
- `ON DUPLICATE KEY UPDATE point = point + 100`처럼 기존 값에 **더하는** 방식으로 UPDATE한 이유
  → 포인트를 새 값으로 덮어쓰는 게 아니라, 기존 포인트에 누적시켜야 하는 요구사항이라 `point + 100`으로 작성함
- `SET @target_continent = "Asia";`로 변수를 만들고 `WHERE Continent = @target_continent`로 사용한 이유
  → 같은 값을 쿼리 여러 곳에서 반복해서 쓸 때, 값을 직접 여러 번 타이핑하지 않고 변수 하나로 관리하기 위함
- `FROM city AS C`, `INNER JOIN country AS CO`처럼 테이블에 짧은 별칭(alias)을 붙인 이유
  → `city.Name`, `country.Name`처럼 두 테이블에 같은 이름의 컬럼(`Name`)이 있어서, 별칭 없이 쓰면
    어느 테이블의 `Name`인지 구분이 안 됨. `C.Name`, `CO.Name`처럼 별칭을 붙여 명확히 구분함
- `ON C.CountryCode = CO.Code`처럼 조인 조건에 서로 **다른 이름의 컬럼**을 쓴 이유
  → city 테이블의 외래키 컬럼명은 `CountryCode`, country 테이블의 기본키 컬럼명은 `Code`로 원래
    이름이 다르기 때문에, JOIN 조건에서는 "값이 같은지"만 확인하면 되고 컬럼명이 똑같을 필요는 없음을 확인함

### 막혔던 부분 / 이해 포인트
- `SELECT "a" + "B" AS A`가 에러 없이 `0`을 반환하는 걸 보고 처음엔 당황했는데, MySQL의 `+`는 파이썬과 달리 **오직 숫자 연산 전용**이라서, 숫자로 변환 안 되는 문자열끼리 더하면 에러 대신 0으로 처리된다는 걸 확인함
  → 문자열을 합치고 싶을 땐 `+`가 아니라 `CONCAT()`을 써야 한다는 걸 이해함
- `WHERE 컬럼명 = NULL`은 항상 결과가 없다는 걸 확인함 (NULL은 "값"이 아니라 "상태"라서 `=`로 비교 자체가 성립 안 함) → `IS NULL`을 써야 한다는 걸 체감함
- INNER JOIN은 `WHERE`, `ORDER BY`, `LIMIT`과 함께 자연스럽게 조합해서 쓸 수 있다는 걸 확인함
  → JOIN으로 두 테이블을 합친 결과를, 마치 하나의 테이블처럼 필터링(WHERE)·정렬(ORDER BY)·개수 제한(LIMIT) 할 수 있음
- `SELECT` 절에서 만든 별칭(alias)은 **같은 SELECT 절 안에서는 재참조가 안 된다**는 걸 확인함
  → SQL은 `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY` 순서로 실행되는데, 별칭은 `SELECT` 단계에서 만들어지므로 같은 `SELECT` 절 내 다른 컬럼 계산에는 아직 쓸 수 없음 (단, `HAVING`이나 `ORDER BY`에서는 `SELECT`보다 늦게 실행되므로 별칭 재사용 가능)

---

## 📅 2026-09-17 | 외부/상호/자체 조인, 인덱스, 뷰, 스토어드 프로시저, 백업·복원, PyMySQL 연동 (SQL 마무리)
> 코드: [`join_outer.sql`](./join_outer.sql), [`join_cross_self.sql`](./join_cross_self.sql), [`index_practice.sql`](./index_practice.sql), [`view_practice.sql`](./view_practice.sql), [`stored_procedure.sql`](./stored_procedure.sql), [`pymysql_study.py`](./pymysql_study.py), [`streamlit_db_basic.py`](./streamlit_db_basic.py), [`streamlit_db_search.py`](./streamlit_db_search.py)

### 개념

**1. 외부 조인 (LEFT / RIGHT OUTER JOIN)**
- LEFT OUTER JOIN: 왼쪽(기준) 테이블의 모든 행 출력, 오른쪽에 매칭 데이터 없으면 NULL로 채움
- RIGHT OUTER JOIN: 오른쪽(기준) 테이블의 모든 행 출력, 왼쪽에 매칭 데이터 없으면 NULL로 채움

**2. 상호 조인 (CROSS JOIN)**
- 조인 조건(ON) 없이 A 테이블의 모든 행과 B 테이블의 모든 행을 1:1로 무조건 조합
- 결과 행 수 = A 행 수 × B 행 수, 주로 성능 테스트·더미 데이터 생성에 활용

**3. 자체 조인 (SELF JOIN)**
- 하나의 테이블 내에서 계층 구조(사원-상사, 카테고리-상위카테고리)를 조회할 때, 자기 자신과 조인
- 한 테이블을 두 번 참조하므로 반드시 서로 다른 별칭(E, M 등) 필요

**4. 인덱스(Index)**
- 데이터를 특정 기준으로 정렬해 피라미드(Tree) 구조로 묶어, 빠르게 찾을 수 있게 하는 장치
- Full Table Scan(인덱스 없을 때, 처음부터 끝까지 다 읽음) vs Index Scan(인덱스로 바로 찾음)
- B-Tree 구조: 루트 노드 → 중간 노드 → 리프 노드, 1억 건이어도 3~4번 이동으로 탐색 완료
- 클러스터형 인덱스(PK 지정 시 자동 생성, 테이블당 1개, 리프 노드에 데이터 전체 저장) vs
  보조 인덱스(여러 개 생성 가능, `CREATE INDEX`로 생성, 리프 노드에 PK 값만 저장)
- `CREATE INDEX 인덱스명 ON 테이블명(컬럼)` / `DROP INDEX 인덱스명 ON 테이블명`
- `EXPLAIN`: SQL 앞에 붙이면 실행 계획(스캔 방식) 확인 가능 (`type=ALL`은 Full Scan, `type=ref`+`key`는 Index Scan)

**5. 뷰(View)**
- 실제 데이터를 저장하지 않고, SELECT 쿼리(정의)만 저장해뒀다가 호출 시 원본 테이블을 조회해 결과 반환하는 가상 테이블
- 디스크 절약 + 원본 데이터 변경 시 즉시 반영(실시간 동기화)
- 활용: 보안(민감 컬럼 제외한 뷰만 접근권한 부여), 복잡한 JOIN 쿼리 재사용
- `CREATE VIEW 뷰이름 AS SELECT ...` / `DROP VIEW 뷰이름`

**6. 스토어드 프로시저(Stored Procedure)**
- 자주 쓰는 SQL 코드를 DB에 미리 저장해두고 `CALL 프로시저명(매개변수)`로 호출하는 "DB 내장 함수"
- `DELIMITER //`로 구분자를 임시 변경(프로시저 내부의 `;`가 SQL을 도중에 끊지 않도록) 후, 정의 끝나면 다시 `;`로 복원
- `DECLARE`(내부 변수 선언), `SET`(고정값 대입), `INTO`(SELECT 결과를 변수에 저장)
- `IN`(입력 매개변수) / `OUT`(출력 매개변수), 매개변수는 `p_`, 내부 변수는 `v_` 접두사 관례

**7. 백업(Backup)과 복원(Restore)**
- 논리적 백업(SQL Dump, `.sql` 텍스트 파일) vs 물리적 백업(디스크 파일 자체 복사)
- Workbench: Server → Data Export(백업) / Data Import(복원)
- 복원 시 `ERROR 1046 (No database selected)`: 백업 파일에 `CREATE DATABASE`/`USE` 구문이 없을 때 발생
  → Data Import 화면의 `Default Target Schema`를 지정하거나, `.sql` 파일 맨 위에 `CREATE DATABASE IF NOT EXISTS ...; USE ...;` 직접 추가

**8. Python-MySQL 연동 (PyMySQL)**
- `pymysql`: 파이썬과 MySQL 간 통신을 담당하는 라이브러리 (`pip install pymysql`)
- 연동 절차: `pymysql.connect(host, user, password, db, charset, cursorclass)` → `conn.cursor()` → `cursor.execute(sql)` → `cursor.fetchall()`
- `cursorclass=pymysql.cursors.DictCursor`: 조회 결과를 `list[dict]` 형태로 받음 (기본은 튜플)
- `fetchone()`(하나만) / `fetchmany(n)`(n개) / `fetchall()`(전체)
- `localhost`는 "내 IP를 자동으로 찾아 적는 것"이 아니라, 컴퓨터 자신을 가리키는 **고정된 예약 주소**(`127.0.0.1`과 동일)

**9. Streamlit + PyMySQL 연동**
- `pymysql`로 조회한 `list[dict]` 결과를 `st.table()`로 바로 웹 화면에 표출 가능
- `cursor.execute(sql, (값1, 값2))`처럼 SQL 안에 `%s` 플레이스홀더를 쓰고 값을 튜플로 따로 전달하면, 사용자 입력값이 SQL 구문에 안전하게 반영됨 (SQL Injection 방지)

### 왜 이렇게 코딩했는가
- 자체 조인(SELF JOIN)에서 같은 테이블(`employees`)을 `e`, `m`이라는 서로 다른 별칭으로 두 번 참조한 이유
  → 하나의 테이블을 "사원 역할"과 "상사 역할" 두 가지로 동시에 다뤄야 하는데, 별칭이 없으면 두 참조를 구분할 방법이 없어서 반드시 별칭이 필요함
- 인덱스 성능 비교 실습에서 `world.city`를 그대로 안 쓰고 `city_test`라는 복사본을 만들어서 실습한 이유
  → 원본 테이블을 건드리지 않고, 인덱스 생성 전/후의 `EXPLAIN` 결과를 안전하게 비교하기 위함
- 뷰(View)를 만들 때 민감 컬럼(`user_ssn`, `salary`)을 제외하고 `user_id`, `user_name`만 선택한 이유
  → 원본 테이블에 대한 접근은 차단하고, 안전한 컬럼만 뷰로 노출해서 보안(접근 통제)을 구현하기 위함
- `pymysql.connect()`에 `cursorclass=pymysql.cursors.DictCursor`를 지정한 이유
  → 기본값(튜플)으로 받으면 순서로만 값에 접근해야 하는데, 딕셔너리로 받으면 `city['Name']`처럼 컬럼명으로 값을 꺼낼 수 있어 가독성이 좋음
- `streamlit_db_search.py`에서 SQL 안에 값을 직접 문자열로 끼워 넣지 않고 `%s` 플레이스홀더를 쓴 이유
  → `cursor.execute(sql, (continent, min_pop))`처럼 값을 따로 전달하면, 사용자 입력값에 특수문자나
    악의적인 SQL 구문이 섞여 들어와도 SQL 자체가 깨지거나 악용되지 않도록 막아주는 효과(SQL Injection 방지)가 있음
- `st.sidebar.selectbox()`로 대륙 선택은 사이드바에, `st.form()`으로 최소 인구수 입력과 검색 버튼은
  메인 화면에 배치한 이유
  → 검색 조건(대륙)은 항상 보이는 사이드바에 고정해두고, 실제 실행을 트리거하는 입력(인구수+버튼)은
    form으로 묶어서 버튼을 누르기 전까지 화면이 매번 새로고침되지 않도록 함

### 막혔던 부분 / 이해 포인트
- `EXPLAIN` 결과에서 `type` 컬럼이 `ALL`(Full Table Scan)에서 `ref`(Index Scan)로 바뀌는 걸 직접 확인하며, 인덱스가 실제로 검색 경로를 바꾼다는 걸 체감함
- 뷰는 `DROP VIEW`를 해도 원본 테이블(`real_user`) 데이터는 그대로 남아있는 걸 확인하며 뷰가 SELECT 쿼리의 "이름표"일 뿐이라는 걸 이해함
- `localhost`가 "내 IP를 자동으로 찾아 적는 것"이 아니라, **컴퓨터 자신을 가리키는 고정된 예약 주소**(`127.0.0.1`과 동일)라는 걸 확인함
- `pymysql`로 접속하는 것도 결국 MySQL Workbench와 똑같이 **같은 MySQL 서버**에 접속하는 것이고, 접속 도구만 다를 뿐 데이터는 같은 곳에 있다는 걸 이해함
- `app.py`에서 `return cursor.fetchall()`을 `with` 블록 안에 두면, `return` 즉시 함수가 종료되어
  그 아래에 있던 `conn.close()`가 실행되지 않는다는 걸 확인함
  → DB 연결을 안전하게 닫으려면, 결과를 먼저 변수에 담고 `with` 블록을 빠져나온 뒤 `conn.close()`를
    호출하고, 그 다음에 `return`해야 한다는 걸 이해함

---

## 📅 2026-09-17 | Streamlit + PyMySQL 연동 실습
> 코드: [`streamlit_db_basic.py`](./streamlit_db_basic.py), [`streamlit_db_search.py`](./streamlit_db_search.py)

### 왜 이렇게 코딩했는가
- `streamlit_db_search.py`에서 SQL 안에 값을 직접 문자열로 끼워 넣지 않고 `%s` 플레이스홀더를 쓴 이유
  → `cursor.execute(sql, (continent, min_pop))`처럼 값을 따로 전달하면, PyMySQL이 안전하게 값을 채워 넣어줌.
    이렇게 하면 사용자 입력값에 특수문자나 악의적인 SQL 구문이 섞여 들어와도 SQL 자체가 깨지거나
    악용되지 않도록 막아주는 효과(SQL Injection 방지)가 있음
- `st.sidebar.selectbox()`로 대륙 선택은 사이드바에, `st.form()`으로 최소 인구수 입력과 검색 버튼은
  메인 화면에 배치한 이유
  → 검색 조건(대륙)은 항상 보이는 사이드바에 고정해두고, 실제 실행을 트리거하는 입력(인구수+버튼)은
    form으로 묶어서 버튼을 누르기 전까지 화면이 매번 새로고침되지 않도록 함
- `st.table(data)`로 조회 결과를 출력한 이유
  → `pymysql`이 `list[dict]` 형태로 반환한 결과를, 별도 가공 없이 바로 표 형태로 웹에 표출하기 위함

### 막혔던 부분 / 이해 포인트
- `app.py`에서 `return cursor.fetchall()`을 `with` 블록 안에 두면, `return` 즉시 함수가 종료되어
  그 아래에 있던 `conn.close()`가 실행되지 않는다는 걸 확인함
  → DB 연결을 안전하게 닫으려면, 결과를 먼저 변수에 담고 `with` 블록을 빠져나온 뒤 `conn.close()`를
    호출하고, 그 다음에 `return`해야 한다는 걸 이해함
- `WHERE CO.Continent = %s AND C.Population >= %s`처럼 SQL 문자열 안에 `%s`를 넣고,
  `cursor.execute(sql, (continent, min_pop))`으로 튜플을 따로 전달하는 방식이 파이썬 f-string으로
  직접 문자열을 조합하는 것과 다르다는 걸 확인함 (f-string으로 직접 조합하면 보안에 취약해짐)

---

