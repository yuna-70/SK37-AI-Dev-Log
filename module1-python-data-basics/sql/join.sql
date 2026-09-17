-- TIL: JOIN 개념 및 INNER JOIN (2026-09-16) — 개념 설명은 README.md 참고

-- INNER JOIN 기본 구문
-- SELECT A.컬럼1, B.컬럼2
-- FROM 테이블A AS A
-- INNER JOIN 테이블B AS B ON A.조인키 = B.조인키;

USE world;

-- 도시 정보(city)와 해당 도시가 속한 국가(country) 정보 결합
-- 아시아 대륙 도시만, 도시 인구 내림차순 상위 5개
SELECT
    C.Name AS 도시명,
    CO.Name AS 국가명,
    CO.Continent AS 대륙,
    C.Population AS 도시인구
FROM city AS C
INNER JOIN country AS CO
    ON C.CountryCode = CO.Code
WHERE CO.Continent = "Asia"
ORDER BY C.Population DESC
LIMIT 5;