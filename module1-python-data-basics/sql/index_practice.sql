-- TIL: 인덱스 생성/삭제, EXPLAIN 실행 계획 비교 (2026-09-17) — 개념 설명은 README.md 참고

USE testdb;

-- 샘플 데이터 준비 (world.city 복사)
CREATE TABLE IF NOT EXISTS city_test AS
SELECT * FROM world.city;

SHOW INDEX FROM city_test;

-- Name 컬럼에 보조 인덱스 생성
CREATE INDEX idx_city_name ON city_test(Name);
SHOW INDEX FROM city_test;

-- 인덱스 삭제
DROP INDEX idx_city_name ON city_test;
SHOW INDEX FROM city_test;

-- [테스트 1] 인덱스 없는 상태 - Full Table Scan (type: ALL)
EXPLAIN SELECT * FROM city_test WHERE Name = "Seoul";

-- [테스트 2] 인덱스 생성 후 - Index Scan (type: ref, key: idx_city_name)
CREATE INDEX idx_city_name ON city_test(Name);
EXPLAIN SELECT * FROM city_test WHERE Name = "Seoul";