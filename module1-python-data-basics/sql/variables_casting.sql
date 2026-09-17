-- TIL: 사용자 정의 변수, 명시적/묵시적 형변환 (2026-09-16) — 개념 설명은 README.md 참고

-- 사용자 정의 변수 (@변수)
USE world;

SET @target_continent = "Asia";

SELECT Name, Continent, Population
FROM country
WHERE Continent = @target_continent
ORDER BY Population DESC
LIMIT 3;

-- 명시적 형변환 (문자열 -> 정수형)
SELECT CAST("100" AS SIGNED) + CAST("200" AS SIGNED) AS 합계;

-- 명시적 형변환 (실수 -> 정수형)
SELECT CAST(123.456 AS SIGNED) AS 정수변환;

-- 묵시적 형변환 (숫자로 변환 가능한 문자열은 자동 계산됨)
SELECT "100" + "200" AS 묵시적합계;

-- 묵시적 형변환 실패 사례 (숫자로 변환 불가 -> 0 처리됨, 에러 아님)
SELECT "a" + "B" AS A;

-- 문자열 연결은 +가 아니라 CONCAT() 사용
SELECT CONCAT("a", "B") AS A;