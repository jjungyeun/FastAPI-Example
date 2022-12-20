from fastapi import Depends
from sqlalchemy.orm import Session

from test_platform import app
from test_platform.config.database import get_db
from test_platform.entity import schema
from test_platform.entity.rdb.models import Member


@app.get(
    "/{member_id}",
    tags=["Member"],
    response_model=schema.MemberBase
)
async def get_members(
        member_id: int,
        db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.id == member_id).first()
    address = "{} {} ({})".format(member.city, member.street, member.zipcode)
    return schema.MemberBase(name=member.name, address=address)
