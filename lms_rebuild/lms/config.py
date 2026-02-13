import os
from dotenv import load_dotenv

def load_config(app):
    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")

    app.config["DB_HOST"] = os.getenv("DB_HOST", "127.0.0.1")
    app.config["DB_PORT"] = int(os.getenv("DB_PORT", "3306"))
    app.config["DB_USER"] = os.getenv("DB_USER", "root")
    app.config["DB_PASSWORD"] = os.getenv("DB_PASSWORD", "")
    app.config["DB_NAME"] = os.getenv("DB_NAME", "pdb")

    app.config["ADMIN_CODE"] = os.getenv("ADMIN_CODE", "")