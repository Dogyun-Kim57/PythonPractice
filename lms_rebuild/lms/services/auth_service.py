from flask import current_app
from ..repositories.members_repo import find_by_uid, insert_member
from ..common.security import hash_password, verify_password

def register(uid: str, pw: str, name: str, admin_code: str = ""):
    if find_by_uid(uid):
        return False, "이미 존재하는 아이디!"

    pw_hash = hash_password(pw)

    role = "user"
    if admin_code and admin_code == current_app.config.get("ADMIN_CODE","7293"):
        role = "admin"

    insert_member(uid, pw_hash, name, role)
    return True, f"{role} 계정으로 회원가입 성공"

def login(uid: str, pw: str):
    """
    로그인 규칙:
    1) uid로 회원 조회
    2) active=0이면 차단
    3) 해시 비밀번호 검증
    4) 성공 시 세션에 넣을 안전한 정보만 반환
    """
    user = find_by_uid(uid)
    if not user:
        return None, "아이디 또는 비밀번호가 틀렸습니다."

    if int(user.get("active", 1)) == 0:
        return None, "비활성화된 계정입니다."

    if not verify_password(pw, user["password"]):
        return None, "아이디 또는 비밀번호가 틀렸습니다."

    safe_user = {
        "id": user["id"],
        "uid": user["uid"],
        "name": user["name"],
        "role": user["role"],
    }
    return safe_user, "로그인 성공"
