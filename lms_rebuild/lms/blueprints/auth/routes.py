from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ...extensions.db import get_conn
from ...services.auth_service import register as register_user
from ...services.auth_service import login as login_user


bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.get("/ping")
def ping():
    return "auth ok"

@bp.get("/whoami")
def whoami():
    conn = get_conn()
    with conn.cursor() as cur:
        cur.execute("SELECT DATABASE() AS db, USER() AS user")
        return cur.fetchone()

@bp.get("/register")
def register_form():
    return render_template("auth/register.html", title="회원가입")

@bp.post("/register")
def register_submit():
    uid = request.form["uid"].strip()
    pw = request.form["pw"]
    name = request.form["name"].strip()
    admin_code = request.form.get("admin_code", "").strip()

    ok, msg = register_user(uid, pw, name, admin_code)

    flash(msg, "success" if ok else "danger")
    return redirect(url_for("auth.register_form"))

@bp.get("/login")
def login_form():
    return render_template("auth/login.html", title="로그인")

@bp.post("/login")
def login_submit():
    uid = request.form["uid"].strip()
    pw = request.form["pw"]

    user, msg = login_user(uid, pw)
    if not user:
        flash(msg, "danger")
        return redirect(url_for("auth.login_form"))

    session["user"] = user
    flash(msg, "success")
    return redirect("/")

@bp.get("/logout")
def logout():
    session.clear()
    flash("로그아웃 완료", "info")
    return redirect("/")