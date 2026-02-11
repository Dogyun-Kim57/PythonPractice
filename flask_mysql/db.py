import pymysql


DB_CONFIG = {
    "host": "127.0.0.1",      # 로컬이면 localhost 또는 127.0.0.1
    "user": "crud_user",
    "password": "crud1234",
    "db": "flask_crud",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
    "autocommit": False,      # ✅ 직접 commit/rollback 제어 (실수 줄이기)
}

def get_connection():
    """
    DB 연결을 반환하는 함수
    - 매번 새 연결을 만들어 반환
    - 실습 CRUD에서는 이 방식이 단순하고 안정적
    """
    return pymysql.connect(**DB_CONFIG)


def execute(query, params=None, fetchone=False, fetchall=False, commit=False):
    """
    ✅ 초보자용 "만능 실행 함수"
    - query: SQL 문자열
    - params: 바인딩 파라미터(tuple or dict)
    - fetchone/fetchall: SELECT 결과 받기 옵션
    - commit: INSERT/UPDATE/DELETE 시 True

    사용 예)
    rows = execute("SELECT * FROM posts", fetchall=True)
    execute("DELETE FROM posts WHERE id=%s", (post_id,), commit=True)
    """
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query, params)

            # SELECT 결과 처리
            if fetchone:
                return cursor.fetchone()
            if fetchall:
                return cursor.fetchall()

        # 변경 쿼면 commit
        if commit:
            conn.commit()

    except Exception as e:
        # 변경 쿼 중 오류 발생 시 rollback
        if conn:
            conn.rollback()
        # 에러를 위로 올려서 app.py에서 보여주거나 로그로 확인
        raise e

    finally:
        if conn:
            conn.close()