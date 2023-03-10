from sqlalchemy import Column, BigInteger, SmallInteger, String, ForeignKey, DateTime, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, backref

from test_platform.config.database import Base
from test_platform.entity.schema.public import OrderStatus, DeliveryStatus


class Member(Base):
    __tablename__ = 'member'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    city = Column(String(30), nullable=False)
    street = Column(String(30), nullable=False)
    zipcode = Column(String(10), nullable=False)
    
    orders = relationship('Order', back_populates='member')

    def __init__(self, member_id, name, city, street, zipcode):
        self.id = member_id
        self.name = name
        self.city = city
        self.street = street
        self.zipcode = zipcode


class Order(Base):
    __tablename__ = 'orders'
    id = Column(BigInteger, primary_key=True, index=True)
    member_id = Column(BigInteger, ForeignKey('member.id'), nullable=False)
    delivery_id = Column(BigInteger, ForeignKey('delivery.id'), nullable=False)
    order_date = Column(DateTime, default=func.now(), nullable=False)
    status = Column(SmallInteger, default=OrderStatus.Order, nullable=False)
    
    member = relationship('Member', back_populates='orders')
    delivery = relationship('Delivery', back_populates='orders')


class Delivery(Base):
    __tablename__ = 'delivery'
    id = Column(BigInteger, primary_key=True, index=True)
    city = Column(String(30), nullable=False)
    street = Column(String(30), nullable=False)
    zipcode = Column(String(10), nullable=False)
    status = Column(SmallInteger, default=DeliveryStatus.Ready)
    
    orders = relationship('Order', back_populates='delivery')


class Item(Base):
    __tablename__ = 'item'
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(30), nullable=False)
    price = Column(Integer, nullable=False)
    stock_quantity = Column(Integer, nullable=False)


class OrderItem(Base):
    __tablename__ = 'order_item'
    id = Column(BigInteger, primary_key=True, index=True)
    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    item_id = Column(BigInteger, ForeignKey('item.id'), nullable=False)
    order_price = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)

    order = relationship('Order', backref=backref('order_item', uselist=False))