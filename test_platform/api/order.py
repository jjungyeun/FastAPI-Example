from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from test_platform import app
from test_platform.config.constants import TAG_NAME_ORDERS
from test_platform.api import api_orders_prefix
from test_platform.config.database import get_db
from test_platform.entity.rdb.models import Item, Order, Delivery, OrderItem
from test_platform.config.exceptions import *
from test_platform.entity.schema.order import OrderBase, OrderCreate
from test_platform.entity.schema.public import DeliveryAddress, OrderStatus, DeliveryStatus
from test_platform.util.crud.crud_util import crud_member, crud_item, crud_order


@app.post(
    api_orders_prefix,
    tags=[TAG_NAME_ORDERS]
)
async def add_order(
        order_create_in: OrderCreate,
        db: Session = Depends(get_db)
):
    # get member & item
    member = crud_member.get_by_id(db, order_create_in.member_id)
    item = crud_item.get_by_id(db, order_create_in.item_id)

    if not member:
        raise HTTPException(status_code=400, detail=str(NoMemberException(member_id=order_create_in.member_id)))
    if not item:
        raise HTTPException(status_code=400, detail=str(NoItemException(item_id=order_create_in.item_id)))

    # raise Exception if stock of item is not enough
    if item.stock_quantity < order_create_in.item_count:
        raise HTTPException(status_code=400,
                            detail=str(ItemStockNotEnoughException(item_id=item.id, quantity=item.stock_quantity)))

    # get Delivery address
    address = DeliveryAddress(order_create_in.delivery_city, order_create_in.delivery_street,
                              order_create_in.delivery_zipcode)
    address.set_with_member(member)

    if address.is_empty():
        raise HTTPException(status_code=400, detail=str(NoDeliveryAddressException()))

    crud_order.create_order(db, order_create_in, address, item)

    db.commit()
    return "success"


@app.get(
    api_orders_prefix,
    tags=[TAG_NAME_ORDERS]
)
async def get_orders(
        db: Session = Depends(get_db)
):
    orders = db.query(Order)
    response = []
    for order in orders:
        member = crud_member.get_by_id(db, order.member_id)
        delivery = db.query(Delivery).filter(Delivery.id == order.delivery_id).first()
        order_item = db.query(OrderItem).filter(OrderItem.order_id == order.id).first()
        item = db.query(Item).filter(Item.id == order_item.item_id).first()

        order_base = OrderBase(id=order.id, member_name=member.name, order_date=order.order_date,
                               order_status=OrderStatus(order.status).name,
                               delivery_status=DeliveryStatus(delivery.status).name,
                               delivery_address="{} {} ({})".format(delivery.city, delivery.street,
                                                                    delivery.zipcode),
                               item_name=item.name, item_count=order_item.count,
                               total_price=order_item.order_price)
        response.append(order_base)

    return response
