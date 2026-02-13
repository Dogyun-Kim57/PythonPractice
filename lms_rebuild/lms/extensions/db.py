import pymysql
from flask import current_app, g


def get_conn():
    if "db_conn" not in g:
        g.db_conn = pymysql.connect(
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False,
        )
    return g.db_conn

def close_conn(e=None):
    conn = g.pop("db_conn", None)
    if conn:
        conn.close()
