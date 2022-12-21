from typing import List, Optional

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from test_platform.api import api_members_prefix
from test_platform import app
from test_platform.config.constants import TAG_NAME_MEMBERS
from test_platform.config.database import get_db
from test_platform.entity.rdb.models import Member
from test_platform.entity.schema.member import MemberBase, MemberCreate
from test_platform.util.crud.crud_util import crud_member


@app.get(
    api_members_prefix + "/{member_id}",
    tags=[TAG_NAME_MEMBERS],
    response_model=MemberBase,
    response_model_exclude_unset=True
)
async def get_member_by_id(
        member_id: int,
        db: Session = Depends(get_db)
):
    member = crud_member.get_by_id(db, member_id)
    return MemberBase(name=member.name, address=(get_address(member)))


@app.get(
    api_members_prefix,
    tags=[TAG_NAME_MEMBERS],
    response_model=List[MemberBase]
)
async def get_members(
        db: Session = Depends(get_db)
):
    members = crud_member.get_all(db)
    response = []
    for member in members:
        response.append(MemberBase(id=member.id, name=member.name, address=get_address(member)))
    return response


@app.post(
    api_members_prefix,
    tags=[TAG_NAME_MEMBERS]
)
async def add_member(
        member_create_in: MemberCreate,
        db: Session = Depends(get_db)
):
    member = Member(member_create_in.id, member_create_in.name, member_create_in.city, member_create_in.street,
                    member_create_in.zipcode)
    db.add(member)
    db.commit()
    return "success"


@app.delete(
    api_members_prefix,
    tags=[TAG_NAME_MEMBERS]
)
async def delete_members(
        member_ids: List[int] = Query(default=..., alias="id", desciption="id=1&member_id=2"),
        db: Session = Depends(get_db)
):
    return await crud_member.bulk_delete(db, member_ids)


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
