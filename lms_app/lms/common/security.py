from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(raw: str) -> str:
    return generate_password_hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    # ✅ 정답: (저장된 해시, 사용자가 입력한 비밀번호)
    return check_password_hash(hashed, raw)