-- TIL: Open API로 수집한 도서 데이터 MySQL 저장/검증 (2026-09-18) — 개념 설명은 README.md 참고

CREATE DATABASE IF NOT EXISTS bookdb
DEFAULT CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE bookdb;

DROP TABLE IF EXISTS book_table;

CREATE TABLE book_table (
    no               INT UNSIGNED NOT NULL,
    ranking          INT UNSIGNED NOT NULL,
    book_name        VARCHAR(255) NOT NULL,
    author           VARCHAR(255) DEFAULT NULL,
    publisher        VARCHAR(100) DEFAULT NULL,
    pub_year         YEAR DEFAULT NULL,
    isbn13           VARCHAR(13) DEFAULT NULL,
    addition_symbol  VARCHAR(5) DEFAULT NULL,
    vol              VARCHAR(20) DEFAULT NULL,
    class_no         VARCHAR(20) DEFAULT NULL,
    class_name       VARCHAR(100) DEFAULT NULL,
    loan_count       INT UNSIGNED DEFAULT 0,
    cover_url        VARCHAR(500) DEFAULT NULL,
    detail_url       VARCHAR(500) DEFAULT NULL,
    PRIMARY KEY (no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 전체 저장된 데이터 개수 확인 (200건 정상 입력 여부)
SELECT COUNT(*) AS 총도서수
FROM book_table;

-- 상위 10위 인기 도서 기본 정보 확인
SELECT ranking AS 순위, book_name AS 도서명, author AS 저자, publisher AS 출판사, loan_count AS 대출건수
FROM book_table
ORDER BY ranking ASC
LIMIT 10;