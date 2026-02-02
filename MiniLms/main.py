from MiniLms.Common.Session import Session
from MiniLms.Service.Member_Service import MemberService


def main():
    service = MemberService()

    uid = input("아이디(uid): ").strip()
    pw = input("비밀번호: ").strip()

    member = service.login(uid, pw)

    if member:
        Session.login(member)
        print(f"\n로그인 성공! 환영합니다, {member.name}님")
        print("현재 세션 사용자:", Session.current_user)
    else:
        print("\n로그인 실패: 아이디/비밀번호가 틀리거나 비활성 계정입니다.")

    print("1) 회원 목록 보기")
    cmd = input("선택: ").strip()

    if cmd == "1":
        members = service.list_members()
        for m in members:
            print(m)





if __name__ == "__main__":
    main()

