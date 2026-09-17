-- TIL: 집계 함수, GROUP BY, HAVING (2026-09-16) — 개념 설명은 README.md 참고

USE world;

-- 집계 함수 (COUNT, SUM, AVG, MAX, MIN)
SELECT
    COUNT(*) AS 전체국가수,
    SUM(Population) AS 전세계총인구수,
    AVG(Population) AS 국가별평균인구,
    MAX(Population) AS 최고인구수,
    MIN(Population) AS 최저인구수
FROM country;

-- GROUP BY: 대륙별 국가 수, 총 인구수, 평균 기대수명
SELECT
    Continent AS 대륙,
    COUNT(*) AS 국가수,
    SUM(Population) AS 총인구수,
    AVG(LifeExpectancy) AS 평균기대수명
FROM country
GROUP BY Continent
ORDER BY 총인구수 DESC;

-- HAVING: 총 인구수가 5억 명 이상인 대륙만 필터링
SELECT
    Continent AS 대륙,
    SUM(Population) AS 총인구수
FROM country
GROUP BY Continent
HAVING 총인구수 >= 500000000
ORDER BY 총인구수 DESC;

-- [실습] world.city: 국가코드별 도시 개수, 10개 이상인 국가코드만
SELECT
    CountryCode,
    COUNT(*) AS 도시수
FROM city
GROUP BY CountryCode
HAVING 도시수 >= 10
ORDER BY 도시수 DESC;

-- [실습] sakila.payment: 고객별 총 결제 금액
USE sakila;

SELECT
    customer_id,
    SUM(amount) AS 총결제금액
FROM payment
GROUP BY customer_id
ORDER BY 총결제금액 DESC;