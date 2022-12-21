from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from test_platform import app
from test_platform.config.database import get_db
from test_platform.entity import schema
from test_platform.entity.rdb.models import Item


@app.get(
    "/items",
    tags=["Item"],
    response_model=List[schema.ItemBase]
)
async def get_items(
        db: Session = Depends(get_db)
):
    items = db.query(Item)
    response = []
    for item in items:
        response.append(schema.ItemBase(id=item.id, name=item.name, price=item.price))
    return response


@app.post(
    "/items",
    tags=["Item"]
)
async def add_item(
        item_create_in: schema.ItemCreate,
        db: Session = Depends(get_db)
):
    item = Item(id=item_create_in.id, name=item_create_in.name, price=item_create_in.price,
                stock_quantity=item_create_in.stock_quantity)
    db.add(item)
    db.commit()
    return "success"

