from ..extensions.db import get_conn

def find_by_uid(uid: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM members WHERE uid=%s", (uid,))
        return cur.fetchone()

def insert_member(uid: str, pw_hash: str, name: str, role: str = "user"):
    """
    members 테이블 스키마 그대로 사용
    """
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO members(uid, password, name, role, active)
                VALUES(%s, %s, %s, %s, 1)
                """,
                (uid, pw_hash, name, role),
            )
        conn.commit()
        print("✅ INSERT 성공: PDB.members")
    except Exception as e:
        conn.rollback()
        print("❌ INSERT 실패(ROLLBACK):", e)
        raise