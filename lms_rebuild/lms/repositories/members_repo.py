from ..extensions.db import get_conn

def find_by_uid(uid: str):
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM members WHERE uid=%s", (uid,))
        return cur.fetchone()

def insert_member(uid: str, pw_hash: str, name: str, role: str):
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
        print("✅ INSERT OK:", uid, role)
    except Exception as e:
        conn.rollback()
        print("❌ INSERT FAIL:", e)
        raise