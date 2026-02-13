from ..repositories.members_repo import find_by_uid, insert_member
from ..common.security import hash_password, verify_password

def register(uid: str, pw: str, name: str, admin_code: str = ""):
    if find_by_uid(uid):
        return False, "이미 존재하는 아이디입니다."
    print("DEBUG service admin_code:", repr(admin_code))
    pw_hash = hash_password(pw)

    # 기본 role
    role = "user"

    # 🔥 관리자 코드 확인
    if admin_code == "admin7293":   # 여기 원하는 코드 지정
        role = "admin"

    insert_member(uid, pw_hash, name, role=role)
    return True, f"{role} 계정으로 회원가입 성공"


def login(uid: str, pw: str):
    """
    로그인 규칙:
    - uid로 회원 조회
    - 비번 해시 검증
    - 성공 시 세션에 넣을 최소 정보만 리턴
    """
    user = find_by_uid(uid)
    if not user:
        return None, "아이디 또는 비밀번호가 틀렸습니다."

    # active가 0이면 로그인 막기(기본기)
    if int(user.get("active", 1)) == 0:
        return None, "비활성화된 계정입니다."

    if not verify_password(pw, user["password"]):
        return None, "아이디 또는 비밀번호가 틀렸습니다."

    # 세션에는 최소한만 (비번 같은 민감정보 절대 저장 X)
    safe_user = {
        "id": user["id"],
        "uid": user["uid"],
        "name": user["name"],
        "role": user["role"],
    }
    return safe_user, "로그인 성공"