-- TIL: DB/테이블 생성·삭제, 제약조건 (2026-09-15) — 개념 설명은 README.md 참고

-- 기존 데이터베이스 확인
SHOW DATABASES;

-- 새로운 데이터베이스 생성
CREATE DATABASE testdb;

-- 사용할 데이터베이스 지정
USE testdb;

-- 테이블 생성
CREATE TABLE test_table (
    col1 INT,
    col2 VARCHAR(50),
    col3 DATETIME
);

-- 결과 확인
SHOW TABLES;

-- 테이블 삭제
DROP TABLE test_table;
SHOW TABLES;

-- PRIMARY KEY, NOT NULL, AUTO_INCREMENT 적용
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL,
    email VARCHAR(100)
);
SHOW TABLES;
DESCRIBE users;

-- 제약조건 종합 적용 테이블 생성 (반복 실습에도 안전하도록 IF EXISTS 사용)
DROP TABLE IF EXISTS test_table;
CREATE TABLE test_table (
    col1 INT PRIMARY KEY AUTO_INCREMENT,
    col2 VARCHAR(50) NOT NULL,
    col3 VARCHAR(100)
);
SHOW TABLES;
DESCRIBE test_table;