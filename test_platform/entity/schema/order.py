from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class OrderBase(BaseModel):
    id: Optional[int]
    member_name: Optional[str]
    order_date: Optional[datetime]
    order_status: Optional[str]
    delivery_status: Optional[str]
    delivery_address: Optional[str]
    item_name: Optional[str]
    item_count: Optional[int]
    total_price: Optional[int]


class OrderCreate(BaseModel):
    id: int = Field(default=..., description="주문 아이디")
    member_id: int = Field(default=..., description="회원 아이디")
    item_id: int = Field(default=..., description="아이템 아이디")
    item_count: int = Field(default=..., gt=0, description="주문할 아이템 개수")
    delivery_city: str = Field(default=None, description="배송 도시")
    delivery_street: str = Field(default=None, description="배송 도로")
    delivery_zipcode: str = Field(default=None, description="배송지 우편번호")

