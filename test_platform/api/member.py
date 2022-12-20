from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from test_platform import app
from test_platform.config.database import get_db
from test_platform.entity import schema
from test_platform.entity.rdb.models import Member


@app.get(
    "/members/{member_id}",
    tags=["Member"],
    response_model=schema.MemberBase,
    response_model_exclude_unset=True
)
async def get_member_by_id(
        member_id: int,
        db: Session = Depends(get_db)
):
    member = db.query(Member).filter(Member.id == member_id).first()
    return schema.MemberBase(name=member.name, address=(get_address(member)))


@app.get(
    "/members",
    tags=["Member"],
    response_model=List[schema.MemberBase]
)
async def get_members(
        db: Session = Depends(get_db)
):
    members = db.query(Member)
    response = []
    for member in members:
        response.append(schema.MemberBase(id=member.id, name=member.name, address=get_address(member)))
    return response


@app.post(
    "/members",
    tags=["Member"]
)
async def add_member(
        member_create_in: schema.MemberCreate,
        db: Session = Depends(get_db)
):
    member = Member(member_create_in.id, member_create_in.name, member_create_in.city, member_create_in.street, member_create_in.zipcode)
    db.add(member)
    db.commit()


def get_address(member):
    address = ""
    if member.city:
        address += member.city

    if member.street:
        if address != "":
            address += " "
        address += member.street

    if address == "":
        address = "No address Info"

    if member.zipcode:
        address += " ({})".format(member.zipcode)

    return address
