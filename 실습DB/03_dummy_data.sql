-- 더미데이터 모음 쿼리 
use PDB;
-- members 더미 데이터
INSERT IGNORE INTO members (id, uid, password, name, role, active, created_at)
VALUES (1,'kdk','7293','김도균','admin',1,'2026-01-28 12:12:03'),
(2,'kdo','7293','도균','manager',1,'2026-01-28 12:12:03'),
(3,'kdd','7293','학생','user',1,'2026-01-28 12:12:08');


DELETE FROM members WHERE uid = 'kdd';
SHOW CREATE TABLE members;
DESC members;
SHOW CREATE TABLE members;
SELECT * FROM members;