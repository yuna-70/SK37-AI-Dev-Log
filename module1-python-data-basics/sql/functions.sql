-- TIL: 문자열/날짜/제어흐름 내장 함수, IS NULL (2026-09-16) — 개념 설명은 README.md 참고

USE world;

-- 문자열 처리 함수
SELECT
    CONCAT(Name, " (", Continent, ")") AS 국가정보,
    UPPER(Name) AS 대문자국가명,
    SUBSTRING(Name, 1, 3) AS 약어
FROM country
LIMIT 5;

-- 날짜 및 시간 처리 함수
SELECT
    NOW() AS 현재시간,
    DATE_ADD(NOW(), INTERVAL 7 DAY) AS 일주일후,
    DATEDIFF("2026-12-31", CURDATE()) AS 남은일수,
    DATE_FORMAT(NOW(), "%Y년 %m월 %d일 %H시") AS 포맷변환;  -- %M,%D(대문자)가 아닌 %m,%d(소문자)로 수정

-- IF, IFNULL
SELECT
    Name,
    LifeExpectancy,
    IF(LifeExpectancy >= 75, "장수국가", "일반국가") AS 국가분류,
    IFNULL(GNPOld, 0) AS 이전GLP
FROM country
LIMIT 5;

-- CASE WHEN
SELECT
    Name, Population,
    CASE
        WHEN Population >= 100000000 THEN "초대형 국가"
        WHEN Population >= 50000000 THEN "중대형 국가"
        ELSE "소형 국가"
    END AS 인구규모분류
FROM country
LIMIT 5;

-- [실습] sakila.film: 대문자 제목 + 대여료 기준 등급 분류, 상위 10개
USE sakila;

SELECT
    UPPER(title) AS 영화제목,
    rental_duration AS 대여기간,
    rental_rate AS 대여료,
    IF(rental_rate >= 3.0, "프리미엄", "일반") AS 요금등급
FROM film
LIMIT 10;