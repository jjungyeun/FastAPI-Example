from typing import Optional

from pydantic import BaseModel


class MemberBase(BaseModel):
    id: Optional[int]
    name: Optional[str]
    address: Optional[str]
