-- TIL: 외부 조인 LEFT/RIGHT OUTER JOIN (2026-09-17) — 개념 설명은 README.md 참고

USE testdb;

CREATE TABLE IF NOT EXISTS j_member (
    user_id VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS j_buy (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id VARCHAR(10),
    prod_name VARCHAR(20)
);

INSERT INTO j_member VALUES ("KIM", "짱구"), ("LEE", "수지");
INSERT INTO j_buy VALUES (NULL, "KIM", "노트북");

-- LEFT JOIN: 구매 이력이 없는 회원 정보도 포함
SELECT
    M.user_id AS 유저아이디,
    M.user_name AS 유저이름,
    B.prod_name AS 상품이름
FROM j_member AS M
LEFT OUTER JOIN j_buy AS B
    ON M.user_id = B.user_id;

-- [종합 실습] 대륙별 도시 인구 합계 (1억 이상, 내림차순)
USE world;

SELECT
    CO.Continent AS 대륙,
    SUM(C.Population) AS 도시인구
FROM country AS CO
INNER JOIN city AS C
    ON CO.Code = C.CountryCode
GROUP BY 대륙
HAVING 도시인구 >= 100000000
ORDER BY 도시인구 DESC;