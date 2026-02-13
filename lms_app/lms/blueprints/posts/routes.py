from flask import Blueprint

bp = Blueprint("posts", __name__)

@bp.get("/")
def home():
    # 지금은 메인화면 테스트용
    return "HOME OK (next: posts list)"