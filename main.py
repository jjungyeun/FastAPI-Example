from enum import Enum
from typing import Union, List, Dict

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# class BrowserName(str, Enum):
#     chrome = "chrome"
#     whale = "whale"
#     safari = "safari"
#
#
# class Item(BaseModel):
#     name: str
#     description: Union[str, None] = None
#     price: float
#     tax: Union[str, None] = None
#
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
#
#
# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
#
#
# @app.get("/items/{item_id}")
# async def read_item(item_id: int, query: Union[str, None] = None):
#     if query:
#         return {"item_id": item_id, "query": query}
#     return {"item_id": item_id}
#
#
# @app.post("/items")
# async def create_item(item: Item):
#     return item
#
#
# @app.get("/browsers/{browser_name}")
# async def get_browser(browser_name: BrowserName):
#     if browser_name is BrowserName.chrome:
#         return {"browser_name": browser_name, "message": "this is chrome"}
#     if browser_name is BrowserName.whale:
#         return {"browser_name": browser_name, "message": "this is whale of Naver"}
#
#     return {"browser_name": browser_name, "message": "this is others"}
#
#
# @app.post("/tags")
# async def create_multiple_tags(tags: List[str]):
#     return tags
#
#
# @app.post("/kv-store")
# async def get_kv_store(kv: Dict[int, str]):
#     return kv
