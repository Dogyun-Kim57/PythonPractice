class Session:
    """
    콘솔 프로그램용 초간단 세션.
    '현재 로그인한 사용자'를 저장한다.
    """
    current_user = None

    @classmethod
    def login(cls, member):
        cls.current_user = member

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls.current_user is not None