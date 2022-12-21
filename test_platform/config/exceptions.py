class NoMemberException(Exception):
    def __init__(self, member_id) -> None:
        super().__init__('해당 회원이 존재하지 않습니다. (회원 아이디: {})'.format(member_id))


class NoItemException(Exception):
    def __init__(self, item_id) -> None:
        super().__init__('해당 아이템이 존재하지 않습니다. (아이템 아이디: {})'.format(item_id))


class ItemStockNotEnoughException(Exception):
    def __init__(self, item_id, quantity) -> None:
        super().__init__('해당 아이템의 재고가 부족합니다. (아이템 아이디: {}, 재고 수량: {})'.format(item_id, quantity))


class NoDeliveryAddressException(Exception):
    def __init__(self) -> None:
        super().__init__('배송지 정보가 없습니다. 배송지를 설정해주세요.')

