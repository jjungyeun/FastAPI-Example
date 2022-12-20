from enum import IntEnum


class OrderStatus(IntEnum):
    Order = 0
    Cancel = 1


class DeliveryStatus(IntEnum):
    Ready = 0
    Comp = 1
