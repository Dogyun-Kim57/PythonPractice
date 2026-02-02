import mysql.connector
from MiniLms.Domain.Member import Member


class MemberService:
    """
    회원 관련 기능 담당 (로그인)
    """

    def __init__(self):
        # ✅ 너 환경에 맞게 수정
        self.db_config = {
            "host": "localhost",
            "user": "root",          # 또는 practice_user
            "password": "Mbc320!!",   # 여기에 입력
            "database": "LMS",
        }

    def login(self, uid: str, password: str) -> Member | None:
        """
        uid/pw로 DB 조회해서 회원을 찾으면 Member 객체 리턴.
        못 찾으면 None.
        """
        sql = """
            SELECT id, uid, name, role, active
            FROM members
            WHERE uid = %s AND password = %s AND active = true
            LIMIT 1
        """

        conn = mysql.connector.connect(**self.db_config)
        try:
            cur = conn.cursor()
            cur.execute(sql, (uid, password))
            row = cur.fetchone()

            if row is None:
                return None

            return Member(
                id=row[0],
                uid=row[1],
                name=row[2],
                role=row[3],
                active=bool(row[4]),
            )
        finally:
            conn.close()

    def list_members(self) -> list[Member]:
        sql = "SELECT id, uid, name, role, active FROM members ORDER BY id"

        conn = mysql.connector.connect(**self.db_config)
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()

            return [
                Member(id=r[0], uid=r[1], name=r[2], role=r[3], active=bool(r[4]))
                for r in rows
            ]
        finally:
            conn.close()
