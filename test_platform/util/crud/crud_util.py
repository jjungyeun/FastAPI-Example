from typing import List, Optional, TypeVar, Type

from pydantic import BaseModel
from sqlalchemy.orm import Session

from test_platform.config.exceptions import NoMemberException
from test_platform.entity.rdb.models import Member, Order, Delivery, OrderItem, Item
from test_platform.entity.schema.order import OrderCreate
from test_platform.entity.schema.public import DeliveryAddress

EntityType = TypeVar('EntityType', bound=BaseModel)


class CrudBase:
    def __init__(self, model: Type[EntityType]):
        self.model = model

    def get_by_id(self, db: Session, id: int) -> Optional[EntityType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_all(self, db: Session) -> List[EntityType]:
        return db.query(self.model)


class CrudMember(CrudBase):
    def __init__(self):
        super().__init__(Member)

    def bulk_delete(self, db: Session, ids: List[int]):
        success_list, failure_list = [], []
        for member_id in ids:
            try:
                member = CrudMember().get_by_id(db, member_id)
                if not member:
                    raise NoMemberException(member_id)
                db.delete(member)
                db.commit()
                success_list.append(member.id)
            except NoMemberException as nme:
                failure_list.append({'id': member_id, 'msg': str(nme)})
            except Exception as e:
                print(e)
                failure_list.append({'id': member_id, 'msg': str(e)})

        return {'success': success_list, 'fail': failure_list}


class CrudOrder(CrudBase):
    def __init__(self):
        super().__init__(Order)

    def create_order(self, db, create_in: OrderCreate, address: DeliveryAddress, item: Item) -> Order:
        # save Delivery & Order
        delivery = Delivery(id=create_in.id, city=address.city, street=address.street, zipcode=address.zipcode)
        order = Order(id=create_in.id, member_id=create_in.member_id, delivery_id=delivery.id)
        order_item = OrderItem(id=create_in.id, order_id=order.id, item_id=item.id,
                               order_price=(create_in.item_count * item.price), count=create_in.item_count)
        db.add(delivery)
        db.add(order)
        db.add(order_item)

        # update Item stock quantity
        db.query(Item).filter(Item.id == item.id).update(
            {"stock_quantity": item.stock_quantity - create_in.item_count})

        return order


class CrudItem(CrudBase):
    def __init__(self):
        super().__init__(Item)


crud_member = CrudMember()
crud_order = CrudOrder()
crud_item = CrudItem()
