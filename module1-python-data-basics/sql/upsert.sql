-- TIL: 조건부 데이터 입력/수정 - INSERT IGNORE, ON DUPLICATE KEY UPDATE (2026-09-16) — 개념 설명은 README.md 참고

USE testdb;

CREATE TABLE IF NOT EXISTS member_point (
    user_id VARCHAR(10) PRIMARY KEY,
    user_name VARCHAR(20),
    point INT
);

-- user_id가 'KIM'인 데이터 삽입/수정(UPSERT) 시도
INSERT INTO member_point VALUES ("KIM", "김철수", 100) ON DUPLICATE KEY UPDATE point = point + 100;

-- 한 번 더 실행하면 'KIM'의 포인트가 200으로 업데이트됨
INSERT INTO member_point VALUES ("KIM", "김철수", 100) ON DUPLICATE KEY UPDATE point = point + 100;

SELECT * FROM member_point;