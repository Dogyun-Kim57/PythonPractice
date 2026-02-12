0) 큰 그림: SQL을 ‘종류’와 ‘목적’으로 나눈다

DB 작업은 크게 3종류가 있어:

DB/테이블 구조 만들기(DDL)

CREATE DATABASE, CREATE TABLE, ALTER, DROP …

데이터 넣고 고치기(DML)

INSERT, UPDATE, DELETE …

데이터 조회(SELECT)

SELECT, JOIN, ORDER BY …

너의 6개 파일은 이 3종류를 “실행 순서 + 기능 목적”에 맞게 나눈 거야.

1) 왜 6개로 나누는 게 좋은가?
✅ 이유 1 — “실행 순서”가 자동으로 정리됨

01 → 02 → 03 순서가 DB 생성 → 테이블 생성 → 데이터 넣기 흐름이잖아.

협업/복습할 때 “뭐부터 실행해야 하지?”가 사라져.

✅ 이유 2 — 실수 방지 (특히 DROP)

DROP DATABASE 같은 위험한 명령은 schema 파일에만 들어가게 하면,
평소 조회/수정 작업할 때 실수로 DB를 날릴 확률이 확 줄어.

✅ 이유 3 — Flask 코드로 옮기기 쉬움

Flask에서 하는 일도 결국

로그인/auth

조회/select

관리자 입력/수정/upsert
처럼 “기능”으로 나뉘거든.

SQL 파일 분리 기준이 Flask 기능 분리 기준과 맞아떨어져.

2) 각 파일의 역할 (한 파일 = 한 책임)
① 01_schema.sql — “DB 그릇” 만들기

목적: DB 자체를 만든다(또는 초기화한다)

포함되는 것:

DROP DATABASE IF EXISTS mini_lms; (연습용 초기화)

CREATE DATABASE mini_lms ...;

USE mini_lms;

SELECT DATABASE(); (검증)

✅ 핵심 포인트

여기엔 테이블 내용이 없어야 좋아.

가장 위험한 DROP DATABASE가 있는 곳이니까, 파일 상단에 경고 주석을 붙이는 습관이 좋음.

② 02_tables.sql — “뼈대(테이블/관계)” 만들기

목적: 프로젝트 구조(테이블, 외래키, 제약조건)를 만든다

포함되는 것:

CREATE TABLE members ...; (부모)

CREATE TABLE scores ... FOREIGN KEY ...; (자식)

CREATE TABLE boards ... FOREIGN KEY ...; (자식)

✅ 핵심 포인트

부모 → 자식 순서로 생성해야 외래키가 걸린다.

삭제할 때는 반대로 자식 → 부모로 DROP 해야 안전하다.

③ 03_dummy_data.sql — “테스트용 데이터” 넣기

목적: 화면/기능 만들 때 바로 확인 가능한 샘플 데이터

포함되는 것:

members 더미 데이터

scores 더미 데이터

(선택) boards 더미 데이터

✅ 핵심 포인트

이 파일은 “개발/연습용”이야.

운영 환경(실제 서비스)에는 보통 실행하지 않음.

④ 04_select_queries.sql — “조회 레시피 모음”

목적: 앱이 화면에 뿌릴 조회 쿼리 모음

포함되는 것:

학생 본인 성적 조회

관리자 전체 조회

정렬/필터(평균순, A학점만 등)

✅ 핵심 포인트

조회는 가장 자주 바뀌고 가장 자주 쓰는 영역이라 따로 모아두면 관리가 쉬움.

WHERE m.uid = ? 처럼 파라미터 자리를 만들어둔 게 핵심.

Flask에서 cursor.execute(sql, (uid,))로 바인딩하면 안전(보안/SQL Injection 방지).

⑤ 05_admin_upsert.sql — “관리자 변경 작업 모음”

목적: 관리자가 하는 “입력/수정/삭제/비활성화” 같은 작업

포함되는 것:

성적 입력/수정(UPSERT)

성적 삭제

학생 비활성화(active=false)

회원 삭제(CASCADE로 scores/boards 같이 삭제)

✅ 핵심 포인트

변경 작업은 실수하면 데이터가 망가질 수 있어서 조회 파일과 분리하는 게 좋아.

특히 DELETE, UPDATE는 관리 작업 영역에만 모아두는 게 안전.

⑥ 06_auth_queries.sql — “로그인/권한” 전용

목적: 인증/인가(권한) 흐름에서 쓰는 쿼리만 모아둔다

포함되는 것:

로그인 확인(아이디/비번/active 체크)

uid 중복 체크

회원가입 insert

role 확인

✅ 핵심 포인트

로그인/회원가입은 앱의 입구라서 다른 SQL이랑 분리하면 관리가 쉬움.

나중에 비밀번호를 해시로 바꾸면(권장), 이 파일에서 주로 수정이 일어남.

3) 실행 순서 (딱 이 순서만 기억하면 됨)
✅ 초기 세팅(처음 1회 or 초기화)

01_schema.sql

02_tables.sql

03_dummy_data.sql

✅ 평소 개발 중(조회/기능 테스트)

보통 04_select_queries.sql, 05_admin_upsert.sql, 06_auth_queries.sql는
“실행해서 DB를 만드는 파일”이 아니라
“쿼리 레시피 참고용”으로 많이 쓴다.

Flask에서 이 쿼리들이 코드로 들어가게 되면, Workbench에서는 테스트할 때만 실행하게 됨.

4) 너가 특히 헷갈릴 포인트 3개 (미리 잡자)
(1) “USE mini_lms;”는 왜 자꾸 넣음?

Workbench에서 다른 DB를 클릭해둔 상태로 쿼리 실행하면, 의도치 않게 다른 DB에 테이블 만들 수도 있어.
그래서 파일 상단에 USE mini_lms;를 박아두면 안전장치가 됨.

(2) “? 파라미터”는 Workbench에서 바로 실행 안 되는데?

맞아. Workbench는 ?에 값을 자동으로 넣어주지 않아서 실행이 불편할 수 있어.
그래서 Workbench 테스트할 때는 임시로:

WHERE m.uid = 'stu01';


이렇게 바꿔서 테스트하고, 저장하기 전에 다시 ?로 되돌리는 방식이 흔해.

(3) DROP이 무서운데… 실전에서는 어떻게 함?

실전(운영)에서는 보통:

01_schema.sql에서 DROP을 빼거나

01_schema_dev.sql(DROP 포함) / 01_schema_prod.sql(DROP 없음)로 분리해.

너도 나중에 “실전용 분리”로 업그레이드하면 된다.

5) 다음으로 이해를 확 올리는 연습(추천)

너가 지금 “이해를 더 해보고 싶다”고 했으니까,
아래 3가지 중 하나만 해도 확 는다:

각 파일을 ‘한 문장’으로 설명해보기

01: DB 만들기

02: 테이블/관계 만들기

03: 더미 넣기

04: 조회 모음

05: 관리자 변경 모음

06: 로그인/권한 모음

“이 기능은 어느 파일로?” 퀴즈 10개 만들어주기 (내가 바로 내줄 수도 있음)

Flask 폴더 구조와 SQL 파일 매핑

auth → 06

student 성적조회 → 04

admin 성적입력/수정 → 05