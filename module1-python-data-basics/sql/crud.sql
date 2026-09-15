-- TIL: 데이터 저장/조회/수정/삭제 (INSERT, SELECT, UPDATE, DELETE) (2026-09-15) — 개념 설명은 README.md 참고

USE testdb;

-- 단일 행 데이터 입력
INSERT INTO test_table (col2, col3) VALUES ("데이터입력1", "2025-01-01");

-- 다중 행 데이터 동시 입력
INSERT INTO test_table (col2, col3) VALUES ("데이터입력2", "2025-01-02"), ("데이터입력3", "2025-01-03");

-- 전체 데이터 조회
SELECT * FROM test_table;

-- 특정 데이터만 수정 (col1이 3인 데이터)
UPDATE test_table SET col2 = "데이터수정" WHERE col1 = 3;
SELECT * FROM test_table;

-- Safe Mode 해제 후 전체 데이터 일괄 수정
SET sql_safe_updates = 0;
UPDATE test_table SET col2 = "전체 데이터 수정";
SELECT * FROM test_table;

-- 조건에 맞는 특정 행 삭제 (col1이 2인 행)
DELETE FROM test_table WHERE col1 = 2;
SELECT * FROM test_table;

-- 테이블 내 전체 데이터 삭제
DELETE FROM test_table;
SELECT * FROM test_table;

-- [종합 실습] 쇼핑몰 회원 DB 구축 및 CRUD 다지기
-- 과제: shopdb 생성, member_tbl 생성, 3건 입력, 홍길동 나이 수정, 강감찬 삭제, 최종 조회

CREATE DATABASE IF NOT EXISTS shopdb;
USE shopdb;

CREATE TABLE member_tbl (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    member_name VARCHAR(20) NOT NULL,
    member_age INT,
    reg_date DATETIME
);

INSERT INTO member_tbl (member_name, member_age, reg_date) VALUES
    ("홍길동", 20, "2026-01-01"),
    ("이순신", 45, "2026-01-02"),
    ("강감찬", 50, "2026-01-03");

UPDATE member_tbl SET member_age = 21 WHERE member_id = 1;
DELETE FROM member_tbl WHERE member_id = 3;
SELECT * FROM member_tbl;