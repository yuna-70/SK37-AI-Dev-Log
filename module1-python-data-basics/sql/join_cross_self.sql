-- TIL: CROSS JOIN, SELF JOIN (2026-09-17) — 개념 설명은 README.md 참고

-- CROSS JOIN 기본 문법 (문법 틀)
-- SELECT A.컬럼1, B.컬럼2
-- FROM 테이블A AS A
-- CROSS JOIN 테이블B AS B;

-- SELF JOIN: 사원-상사 계층 구조 조회
SELECT
    e.name AS 사원이름,
    m.name AS 상사이름
FROM employees AS e
INNER JOIN employees AS m
    ON e.manager_id = m.id;