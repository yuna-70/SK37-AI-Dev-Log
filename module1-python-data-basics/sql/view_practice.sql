-- TIL: 뷰(View) 생성/조회/삭제, 보안 활용 (2026-09-17) — 개념 설명은 README.md 참고

USE testdb;

-- 실습용 원본 테이블 (민감정보 포함)
CREATE TABLE IF NOT EXISTS real_user (
    user_id VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(20) NOT NULL,
    user_ssn VARCHAR(14),   -- 주민번호 (민감정보)
    salary INT              -- 급여 (민감정보)
);

INSERT INTO real_user VALUES
    ("KIM", "짱구", "950101-1234567", 4000000),
    ("LEE", "수지", "980202-2345678", 3500000);

-- 보안용 뷰 생성 (민감 컬럼 제외)
CREATE VIEW v_user_security AS
SELECT user_id, user_name
FROM real_user;

SELECT * FROM v_user_security;

-- 뷰 삭제 (삭제해도 원본 데이터는 유지됨)
DROP VIEW v_user_security;
SELECT * FROM real_user;

-- 복잡한 JOIN을 재사용하는 뷰 (아시아 대륙 도시)
USE world;

CREATE VIEW v_info_continent AS
SELECT
    C.Name AS city_name,
    CO.Name AS country_name,
    C.Population AS city_population
FROM city AS C
INNER JOIN country AS CO
    ON C.CountryCode = CO.Code
WHERE CO.Continent = "Asia";

SELECT * FROM v_info_continent
WHERE city_population >= 5000000
ORDER BY city_population DESC;