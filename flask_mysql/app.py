from flask import Flask, render_template, request, redirect, url_for, flash
from db import execute

app = Flask(__name__)

# ✅ flash 메시지를 쓰려면 secret_key가 필요함
# 실습용: 아무 문자열이나 가능하지만, 실제 서비스에서는 안전한 키 사용
app.secret_key = "dev-secret-key"


@app.route("/")
def home():
    """
    홈에 들어오면 게시글 목록으로 보내기
    """
    return redirect(url_for("post_list"))


# 1) 목록(Read - list)
@app.route("/posts")
def post_list():
    """
    게시글 전체 목록 조회
    """
    posts = execute(
        "SELECT id, title, created_at FROM posts ORDER BY id DESC",
        fetchall=True
    )
    return render_template("list.html", posts=posts)


# 2) 상세(Read - detail)
@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    """
    게시글 1개 상세 조회
    """
    post = execute(
        "SELECT * FROM posts WHERE id = %s",
        (post_id,),
        fetchone=True
    )

    # 존재하지 않는 id면 안내
    if not post:
        flash("존재하지 않는 게시글입니다.")
        return redirect(url_for("post_list"))

    return render_template("detail.html", post=post)


# 3) 작성(Create) - 폼 화면
@app.route("/posts/new", methods=["GET"])
def post_new_form():
    """
    새 글 작성 폼 화면
    """
    return render_template("form.html")


# 3) 작성(Create) - 실제 저장
@app.route("/posts/new", methods=["POST"])
def post_create():
    """
    폼에서 받은 데이터를 DB에 INSERT
    """
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    # ✅ 초보 실수 방지: 빈 값 체크
    if not title or not content:
        flash("제목과 내용은 필수입니다.")
        return redirect(url_for("post_new_form"))

    execute(
        "INSERT INTO posts (title, content) VALUES (%s, %s)",
        (title, content),
        commit=True
    )

    flash("게시글이 작성되었습니다.")
    return redirect(url_for("post_list"))


# 4) 수정(Update) - 폼 화면
@app.route("/posts/<int:post_id>/edit", methods=["GET"])
def post_edit_form(post_id):
    """
    수정 폼 화면: 기존 데이터를 불러와서 form에 채워줌
    """
    post = execute(
        "SELECT * FROM posts WHERE id = %s",
        (post_id,),
        fetchone=True
    )
    if not post:
        flash("존재하지 않는 게시글입니다.")
        return redirect(url_for("post_list"))

    return render_template("edit.html", post=post)


# 4) 수정(Update) - 실제 반영
@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def post_update(post_id):
    """
    수정 폼에서 받은 데이터로 UPDATE
    """
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title or not content:
        flash("제목과 내용은 필수입니다.")
        return redirect(url_for("post_edit_form", post_id=post_id))

    execute(
        "UPDATE posts SET title=%s, content=%s WHERE id=%s",
        (title, content, post_id),
        commit=True
    )

    flash("게시글이 수정되었습니다.")
    return redirect(url_for("post_detail", post_id=post_id))


# 5) 삭제(Delete)
@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def post_delete(post_id):
    """
    삭제는 GET으로 하지 말고(실수/보안), POST로만 처리하는 습관
    """
    execute(
        "DELETE FROM posts WHERE id=%s",
        (post_id,),
        commit=True
    )

    flash("게시글이 삭제되었습니다.")
    return redirect(url_for("post_list"))


if __name__ == "__main__":
    # ✅ debug=True는 개발 중에만!
    app.run(debug=True)