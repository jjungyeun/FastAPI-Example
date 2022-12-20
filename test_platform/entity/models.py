from sqlalchemy import Column, BigInteger, SmallInteger, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from test_platform.config.database import Base
from test_platform.entity.public import OrderStatus, DeliveryStatus


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
