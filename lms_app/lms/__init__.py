
# 이곳은 앱 조립 공장의 개념!
# 설정을 로딩(config)하고, 라우트 묶음(blueprint)을 등록한다.
# 또한, 앱 종료/요청 종료 시 정리 작업(DB close)을 연결한다.

# 설치 파일
# Flask
# PyMySQL
# python-dotenv
# Werkzeug (Flask에 포함되지만 명시적으로 써도 좋음)

# 설치 명령어
# pip install Flask PyMySQL python-dotenv
# pip freeze > requirements.txt ( 해당 프로젝트에 설치된 요소들을 볼 수 있다. )

# 설치 확인
# pip list

# 패키지	역할
# Flask	웹 프레임워크
# PyMySQL	MySQL 연결
# python-dotenv	.env 파일 읽기
# venv	프로젝트 격리

from flask import Flask
from .config import load_config
from .extensions.db import close_conn

from .blueprints.auth import bp as auth_bp

def create_app():
    # ✅ templates/static을 자동으로 lms/templates, lms/static에서 찾게 됨
    app = Flask(__name__, instance_relative_config=True)

    load_config(app)

    # ✅ 블루프린트 등록
    app.register_blueprint(auth_bp)

    # ✅ 메인 페이지(404 방지)
    @app.get("/")
    def home():
        return "HOME OK (PDB 기준 회원가입 테스트: /auth/register)"

    # ✅ 요청 끝날 때 DB 연결 닫기
    app.teardown_appcontext(close_conn)

    return app