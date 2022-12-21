from typing import Optional

from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    price: Optional[int]


class ItemCreate(BaseModel):
    id: int = Field(default=..., description="아이템 아이디")
    name: str = Field(default=..., max_length=30, description="아이템 이름")
    price: int = Field(default=..., ge=1000, description="아이템 개당 가격")
    stock_quantity: int = Field(default=..., ge=1, description="아이템 재고량")

