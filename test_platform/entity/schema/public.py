from enum import IntEnum


class OrderStatus(IntEnum):
    Order = 0
    Cancel = 1


class DeliveryStatus(IntEnum):
    Ready = 0
    Comp = 1


class DeliveryAddress:
    city: str = None
    street: str = None
    zipcode: str = None

    def __init__(self, city, street, zipcode):
        self.city = city
        self.street = street
        self.zipcode = zipcode

    def set_with_member(self, member):
        self.city = self.city if self.city else member.city
        self.street = self.street if self.street else member.street
        self.zipcode = self.zipcode if self.zipcode else member.zipcode

    def is_empty(self):
        return not self.city or not self.street or not self.zipcode
