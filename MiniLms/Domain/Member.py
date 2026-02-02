class Member:
    """
    DB members 테이블의 '한 행'을 파이썬 객체로 표현한 것.
    """
    def __init__(self, id: int, uid: str, name: str, role: str, active: bool):
        self.id = id
        self.uid = uid
        self.name = name
        self.role = role
        self.active = active

    def __repr__(self):
        return (
            f"Member(id={self.id}, uid='{self.uid}', name='{self.name}', "
            f"role='{self.role}', active={self.active})"
        )

