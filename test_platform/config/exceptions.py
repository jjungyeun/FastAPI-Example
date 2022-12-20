class NoMemberException(Exception):
    def __init__(self, member_id) -> None:
        super().__init__('해당 회원이 존재하지 않습니다. (회원 아이디: {})'.format(member_id))