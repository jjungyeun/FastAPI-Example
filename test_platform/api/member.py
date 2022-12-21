from typing import List, Optional

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from test_platform.api import api_members_prefix
from test_platform import app
from test_platform.config.constants import TAG_NAME_MEMBERS
from test_platform.config.database import get_db
from test_platform.config.exceptions import NoMemberException
from test_platform.entity import schema
from test_platform.entity.rdb.models import Member


@app.get(
    api_members_prefix + "/{member_id}",
    tags=[TAG_NAME_MEMBERS],
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
    api_members_prefix,
    tags=[TAG_NAME_MEMBERS],
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
    api_members_prefix,
    tags=[TAG_NAME_MEMBERS]
)
async def add_member(
        member_create_in: schema.MemberCreate,
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
    success_list, failure_list = [], []
    for member_id in member_ids:
        try:
            member = db.query(Member).filter(Member.id == member_id).first()
            if not member:
                raise NoMemberException(member_id)
            db.delete(member)
            db.commit()
            success_list.append(member.id)
        except NoMemberException as nme:
            failure_list.append({'id': member_id, 'msg': str(nme)})
        except Exception as e:
            print(e)
            failure_list.append({'id': member_id, 'msg': str(e)})

    return {'success': success_list, 'fail': failure_list}


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
