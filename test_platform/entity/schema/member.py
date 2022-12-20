from typing import Optional

from pydantic import BaseModel, Field


class MemberBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    address: Optional[str]


class MemberCreate(BaseModel):
    id: int = Field(default=..., description="회원 아이디")
    name: str = Field(default=..., description="회원 이름")
    city: Optional[str] = Field(default=None, description="거주 도시")
    street: Optional[str] = Field(default=None, description="거주 도로")
    zipcode: Optional[str] = Field(default=None, description="거주지 우편번호")