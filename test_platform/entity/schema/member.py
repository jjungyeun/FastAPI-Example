from typing import Optional

from pydantic import BaseModel


class MemberBase(BaseModel):
    name: Optional[str]
    address: Optional[str]
