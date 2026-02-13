from flask import Flask
from .config import load_config
from .extensions.db import close_conn
from .blueprints.auth import bp as auth_bp
from flask import render_template

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    load_config(app)

    app.register_blueprint(auth_bp)

    @app.get("/")
    def home():
        return render_template("home.html", title="홈")

    app.teardown_appcontext(close_conn)
    return app