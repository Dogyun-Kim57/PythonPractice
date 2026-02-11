
-- 사용할 DB생성 -- 
CREATE DATABASE practice_db;

 
-- member 테이블 (객체명 : members)--
CREATE TABLE members (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- 회원 고유 번호
    uid VARCHAR(50) NOT NULL UNIQUE,          -- 로그인 아이디 (중복 불가)
    password VARCHAR(255) NOT NULL,           -- 비밀번호
    name VARCHAR(50) NOT NULL,                -- 이름
    role ENUM('admin','user') DEFAULT 'user', -- 권한
    active BOOLEAN DEFAULT TRUE,              -- 활성화 여부
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 생성 시간
    updated_at DATETIME 
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP           -- 수정 시간 (자동 갱신)
);

-- 게시판 테이블 (객체명 : boards)--
CREATE TABLE boards (
    id INT AUTO_INCREMENT PRIMARY KEY,        -- 게시글 번호
    member_id INT NOT NULL,                   -- 작성자 (members.id를 참조해야하는 외래키)
    title VARCHAR(255) NOT NULL,              -- 제목
    content TEXT NOT NULL,                    -- 내용
    views INT DEFAULT 0,                      -- 조회수
    active TINYINT(1) DEFAULT 1,          -- 삭제 여부 
											  -- 1 = 정상 , 0 = 삭제처리
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 작성 시간
    updated_at DATETIME 
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,          -- 수정 시간

  -- 외래키 설정 (관계 무결성 유지)
  -- member_id는 members 테이블의 id를 참조
  -- 회원 삭제 시 해당 회원의 게시글도 같이 삭제 (CASCADE)

    CONSTRAINT fk_boards_member
        FOREIGN KEY (member_id)
        REFERENCES members(id)
        ON DELETE CASCADE
);



-- 댓글/대댓글 테이블 (객체명 : board_comments)--
-- ==========================================================
-- board_comments 테이블
-- 댓글 + 대댓글(1-depth만 허용) 구조
--
-- parent_id가 NULL이면 일반 댓글 (depth = 0)
-- parent_id가 값이 있으면 대댓글 (depth = 1)
-- ==========================================================
CREATE TABLE board_comments (
  id INT AUTO_INCREMENT PRIMARY KEY,        -- AUTO_INCREMENT: 자동 증가
  board_id INT NOT NULL,					-- board_id: 어떤 게시글에 달린 댓글인지
  member_id INT NOT NULL,					-- member_id: 댓글 작성자
  parent_id INT NULL,						--  parent_id: 부모 댓글 ID
											--  NULL이면 일반 댓글
                                            --  값이 있으면 대댓글 (부모 댓글의 id)
											-- 자기 자신(board_comments.id)을 참조하는 Self-Join 구조
  content TEXT NOT NULL,					-- content: 댓글 내용
  
  depth TINYINT NOT NULL DEFAULT 0,			    -- 🔹 depth:
												-- 0 = 댓글
												-- 1 = 대댓글
												-- 본 프로젝트는 1-depth까지만 허용
   active TINYINT(1) DEFAULT 1,          
  
      -- created_at: 생성 시간
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- updated_at: 수정 시간
    -- UPDATE 발생 시 자동 갱신
    updated_at DATETIME
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

 
    -- 외래키 설정 (관계 무결성 유지)
    -- 게시글 연결
	CONSTRAINT fk_comments_board
        FOREIGN KEY (board_id)
        REFERENCES boards(id)
        ON DELETE CASCADE,

    -- 작성자 연결
    CONSTRAINT fk_comments_member
        FOREIGN KEY (member_id)
        REFERENCES members(id)
        ON DELETE CASCADE,

    -- 부모 댓글 연결 (Self-Reference)
    CONSTRAINT fk_comments_parent
        FOREIGN KEY (parent_id)
        REFERENCES board_comments(id)
        ON DELETE CASCADE,

    -- ==================================================
    -- depth 제한 (0 또는 1만 허용)
    -- ==================================================
    CONSTRAINT chk_depth
        CHECK (depth IN (0, 1))
);

-- ==========================================================
-- 댓글 목록 조회 최적화용 인덱스
-- 게시글 단위 + 부모댓글 정렬 + 시간순 정렬 최적화
-- ==========================================================
CREATE INDEX idx_comments_board_parent_created
ON board_comments (board_id, parent_id, created_at);


-- 점수확인 테이블 (객체명 : scores )--

CREATE TABLE scores (

    id INT AUTO_INCREMENT PRIMARY KEY,

    student_id INT NOT NULL,

    korean INT NOT NULL,
    english INT NOT NULL,
    math INT NOT NULL,

    total INT NOT NULL,

    average DECIMAL(5,2) NOT NULL,   -- avg 대신 average 사용

    grade VARCHAR(5) NOT NULL,

    active TINYINT(1) DEFAULT 1,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    CONSTRAINT fk_scores_student
        FOREIGN KEY (student_id)
        REFERENCES members(id)
        ON DELETE CASCADE
);

-- 강의 정보 테이블 (객체명 : lectures )
CREATE TABLE lectures (
    --  id: 강의 고유 번호
    -- AUTO_INCREMENT: 강의가 추가될 때마다 자동 증가
    -- PRIMARY KEY: 강의를 구분하는 기본 키
    id INT AUTO_INCREMENT PRIMARY KEY,
     title VARCHAR(255) NOT NULL,              -- 강의명  
	 teacher_name VARCHAR(100) NOT NULL,      -- 강사 이름
	 description TEXT,                        -- 강의 설명
	 capacity INT NOT NULL,                  -- 수강 가능 인원 수
     start_date DATE NOT NULL,               -- 강의 시작일 
     end_date DATE NOT NULL,                 -- 강의 종료일
     active TINYINT(1) DEFAULT 1,            -- 운영에 관한 활성 여부 1 = 활성 0 = 비활성 ( 종료 등 )
	 created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 생성 시간
     updated_at DATETIME                     -- 수정 시간
        DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP,

    --  날짜 유효성 체크
    -- 종료일은 시작일보다 빠를 수 없음
    CONSTRAINT chk_date
        CHECK (end_date >= start_date)
);

-- 강의 신청 테이블 (객체명 : enrollments  )
CREATE TABLE enrollments (

    -- id: 수강 신청 고유 번호
    -- AUTO_INCREMENT: 자동 증가
    -- PRIMARY KEY: 신청 레코드 구분
    id INT AUTO_INCREMENT PRIMARY KEY,

    -- lecture_id: 어떤 강의에 신청했는지
    -- lectures.id 참조
    lecture_id INT NOT NULL,

    -- member_id: 누가 신청했는지
    -- members.id 참조
    member_id INT NOT NULL,

    -- status: 신청 상태
    -- APPLIED = 신청 완료
    -- CANCELLED = 신청 취소
    status ENUM('APPLIED', 'CANCELLED') 
        DEFAULT 'APPLIED',

    -- 🔹 applied_at: 신청 날짜
    -- 신청 시 자동 현재 시간 저장
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- ==================================================
    -- 외래키 설정 (무결성 유지)
    -- ==================================================

    -- 강의 삭제 시 해당 신청도 삭제
    CONSTRAINT fk_enroll_lecture
        FOREIGN KEY (lecture_id)
        REFERENCES lectures(id)
        ON DELETE CASCADE,

    -- 회원 삭제 시 해당 신청도 삭제
    CONSTRAINT fk_enroll_member
        FOREIGN KEY (member_id)
        REFERENCES members(id)
        ON DELETE CASCADE,

    -- ==================================================
    -- 중복 신청 방지
    -- 같은 회원이 같은 강의를 두 번 신청 못함
    -- 그래서 고유값을 지정
    -- ==================================================
    CONSTRAINT uq_enrollment UNIQUE (lecture_id, member_id)

);





-- 생성한 DB 사용 --
USE practice_db;


-- db 삭제 --
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS lectures;
DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS board_comments; 			  
DROP TABLE IF EXISTS boards;			   
DROP TABLE IF EXISTS members;              


-- db 확인 --
DESC members;
DESC boards;
DESC board_comments;
DESC scores;
DESC lectures;
DESC enrollments;


-- db 상세 확인 --
SHOW CREATE TABLE members;
SHOW CREATE TABLE boards;
SHOW CREATE TABLE board_comments;
SHOW CREATE TABLE scores;
SHOW CREATE TABLE lectures;
SHOW CREATE TABLE enrollments;



-- 전체 db 확인 --
SHOW TABLES;                   -- 목록에 테이블 있는지 확인 --


