# 파이썬과 mysql 병합 작업을 위한 sql 페이지
# 절차 일반적으로 system(root)계정은 개발용으로 사용하지 않는다.
# mysql에 사용할 id와 pw와 권한을 부여하고 db를 생성한다.

-- 유저 추가 --
CREATE USER 'kdg'@'192.168.0.153' IDENTIFIED BY '1234';
CREATE USER 'practice'@'localhost' IDENTIFIED BY '1234';

SELECT user, host
FROM mysql.user;

-- DB 생성 --
CREATE DATABASE PDB 
default character set utf8mb4 
collate utf8mb4_general_ci;
-- ''라는 데이터베이스를 생성           한국어 지원 utf-8   
-- COLLATE : 문자 집합에 포함된 문자들을 어떻게 비교하고 정렬할지 정의하는 키워드
-- 데이터비교시 대소문자 구분 , 문자 간의 정렬 순서, 언어별 특수문자 처리 방식 지원
-- utf8mb4 : 문자집합 
-- general : 비교규칙(간단한 일반비교)
-- ci : Case Insensitive (대소문자 구분하지 않음)
-- cs : case sensitive (대소문자 구분함 )


-- 유저 삭제 --
drop user 'Pracitice'@'localhost';



-- 사용할 계정 생성 
CREATE USER 'practice'@'localhost' IDENTIFIED BY '1234';
-- 권한 부여
GRANT ALL PRIVILEGES ON PDB.* to 'practice'@'localhost';
-- 권한 부여  모든권한       DB명. *모든 테이블   ID@접속권한범주
-- GRANT : 권한부여 
-- ALL PRIVILEGES ON : 모든 권한
-- mbc.* : mbc라는 db의 모든 테이블
-- to ''@''; : 권한을 받을 계정 정보



-- 즉시 권한 부여
FLUSH PRIVILEGES     





