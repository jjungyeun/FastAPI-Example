from typing import List

from fastapi import Depends
from sqlalchemy.orm import Session

from test_platform.api import api_items_prefix
from test_platform import app
from test_platform.config.constants import TAG_NAME_ITEMS
from test_platform.config.database import get_db
from test_platform.entity.rdb.models import Item
from test_platform.entity.schema.item import ItemBase, ItemCreate


@app.get(
    api_items_prefix,
    tags=[TAG_NAME_ITEMS],
    response_model=List[ItemBase]
)
async def get_items(
        db: Session = Depends(get_db)
):
    items = db.query(Item)
    response = []
    for item in items:
        response.append(ItemBase(id=item.id, name=item.name, price=item.price))
    return response


@app.post(
    api_items_prefix,
    tags=[TAG_NAME_ITEMS]
)
async def add_item(
        item_create_in: ItemCreate,
        db: Session = Depends(get_db)
):
    item = Item(id=item_create_in.id, name=item_create_in.name, price=item_create_in.price,
                stock_quantity=item_create_in.stock_quantity)
    db.add(item)
    db.commit()
    return "success"

