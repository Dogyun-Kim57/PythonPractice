from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(raw: str) -> str:
    return generate_password_hash(raw)

def verify_password(raw: str, hashed: str) -> bool:
    # ✅ (저장된 해시, 입력 비번)
    return check_password_hash(hashed, raw)

