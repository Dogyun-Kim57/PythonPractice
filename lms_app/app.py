# app.py
# - 이 프로그램을 실행하는 시작점 ( Entry Point )

from lms import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

