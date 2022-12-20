from pydantic import BaseSettings
from fastapi import FastAPI


class Settings(BaseSettings):
    class Rdb:
        scheme: str = "postgresql://"
        id: str = "testuser"
        pw: str = "testuser!"
        host: str = "localhost:5432"
        db_name: str = "testdb"


def initialize():
    from test_platform.config.database import Base, engine
    # RDB initialize
    # Create Tables
    Base.metadata.create_all(bind=engine)
    # Drop Tables
    Base.metadata.create_all(bind=engine)


settings = Settings()

# Fast API 초기화
app = FastAPI()
initialize()

from test_platform import api, config, entity, util
