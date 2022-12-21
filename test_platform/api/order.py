from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from test_platform import app
from test_platform.config.database import get_db
from test_platform.entity import schema
from test_platform.entity.rdb.models import Item, Order, Member, Delivery, OrderItem
from test_platform.config.exceptions import *


@app.post(
    "/orders",
    tags=["Order"]
)
async def add_order(
        order_create_in: schema.OrderCreate,
        db: Session = Depends(get_db)
):
    # get member & item
    member = db.query(Member).filter(Member.id == order_create_in.member_id).first()
    item = db.query(Item).filter(Item.id == order_create_in.item_id).first()

    if not member:
        raise HTTPException(status_code=400, detail=str(NoMemberException(member_id=order_create_in.member_id)))
    if not item:
        raise HTTPException(status_code=400, detail=str(NoItemException(item_id=order_create_in.item_id)))

    # raise Exception if stock of item is not enough
    if item.stock_quantity < order_create_in.item_count:
        raise HTTPException(status_code=400, detail=str(ItemStockNotEnoughException(item_id=item.id, quantity=item.stock_quantity)))

    # get Delivery address
    delivery_city = order_create_in.delivery_city if order_create_in.delivery_city else member.city
    delivery_street = order_create_in.delivery_street if order_create_in.delivery_street else member.street
    delivery_zipcode = order_create_in.delivery_zipcode if order_create_in.delivery_zipcode else member.zipcode

    if not delivery_city or not delivery_street or not delivery_zipcode:
        raise HTTPException(status_code=400, detail=str(NoDeliveryAddressException()))

    # save Delivery & Order
    delivery = Delivery(id=order_create_in.id, city=delivery_city, street=delivery_street, zipcode=delivery_zipcode)
    order = Order(id=order_create_in.id, member_id=order_create_in.member_id, delivery_id=delivery.id)
    order_item = OrderItem(id=order_create_in.id, order_id=order.id, item_id=item.id,
                           order_price=(order_create_in.item_count * item.price), count=order_create_in.item_count)
    db.add(delivery)
    db.add(order)
    db.add(order_item)

    # update Item stock quantity
    db.query(Item).filter(Item.id == item.id).update({"stock_quantity": item.stock_quantity - order_create_in.item_count})

    db.commit()
    return "success"
