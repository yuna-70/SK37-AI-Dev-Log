-- TIL: 스토어드 프로시저 문법 정리 (2026-09-17) — 개념 설명은 README.md 참고

-- 기본 문법 구조 (틀)
-- DELIMITER //
-- CREATE PROCEDURE 프로시저명(
--     IN p_입력변수 데이터타입,
--     OUT p_출력변수 데이터타입
-- )
-- BEGIN
--     DECLARE v_변수 데이터타입;
--     SET v_변수 = 값;
--     SELECT 컬럼 INTO v_변수 FROM 테이블 WHERE 조건;
-- END //
-- DELIMITER ;

-- 호출 방식
-- CALL 프로시저명(매개변수);