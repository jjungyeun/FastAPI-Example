from fastapi import Depends
from sqlalchemy.orm import Session

from test_platform import app
from test_platform.config.database import get_db
from test_platform.entity.rdb.models import Member


@app.get(
    "/",
    tags=["Member"]
)
def get_members(
        db: Session = Depends(get_db)
):
    members = db.query(Member)

    response = []
    for member in members:
        response.append(member.name)
    return response