-- TIL: WHERE 조건절, BETWEEN/IN/LIKE (2026-09-15) — 개념 설명은 README.md 참고

USE world;

-- country 테이블의 특정 컬럼 조회
SELECT Name, Continent, Population FROM country;

-- 인구가 1억 명 이상인 국가
SELECT Name, Continent, Population
FROM country
WHERE Population >= 100000000;

-- 대륙이 Asia이면서 인구가 5천만 명 이상인 국가 (AND)
SELECT Name, Continent, Population
FROM country
WHERE Continent = "Asia" AND Population >= 50000000;

-- 인구가 1천만 ~ 2천만 사이인 국가 (BETWEEN)
SELECT Name, Population
FROM country
WHERE Population BETWEEN 10000000 AND 20000000;

-- 대륙이 Asia, Europe, North America 중 하나인 국가 (IN)
SELECT Name, Continent
FROM country
WHERE Continent IN ("Asia", "Europe", "North America");

-- 국가명이 "South"로 시작하는 국가 (LIKE)
SELECT Name
FROM country
WHERE Name LIKE "South%";